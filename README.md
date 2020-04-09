# Example de config Rasa
## Lancement de la stack Docker
Detail des containers de la stack docker-compose :

### Rasa-X
* rasa-x : Héberge la webapp Rasa-X
* Nginx: sert de front pour rasa-x
* db: bdd de rasa-x
* rabbit: message broker pour stocker les conversations du chatbot
* reddis: surement utilisé pour le cache, stockage de la session de rasa-x

### Composants
* Duckling : Composant qui renvoi une analyze des emails, numbers, cardinlos etc...

### Rasa
#### Models
* Rasa-production : Master faisant tourner les models
* Rasa-worker : Slave faisant tourner les models

#### Actions
* app: fait tourner l'api des actions

## Lancement
```bash
docker-compose up -d
```
Attendre le lancement de rasa-x (dispo sur http://localhost)

Changer le pass de rasa-x
```bash
 python rasa-x/rasa_x_commands.py create --update admin me <my_password>
```
Se connecter sur http://localhost

## Développement
* Lancer le docker-compose
* se connecter à rasa-x
* upload manuellement ou fournir à rasa-x les identifiants vers votre repi github/gitlab
* rasa-x recupere toutes les infos(un refresh F5 permet de vérifier la synchro avec le repo distant)
* trainer les models
* tester via le webchat de rasa-x

Votre fichier actions.py est envoyé directement dans le serveur d'actions, si vous effectuez des changement lancez : `docker-compose restart app` afin de lui faire redemarer le container, bien sûr, cela ne sert que quand vous utilisez rasa-x, en shell/interactive rasa utilise le fichiers actions.py directement en local


La stack docker-compose utilise un Dockerfile pour construire le "serveur" d'actions(voir `rasa-x/docker/app/Dockerfile`)  
Le but de cette image est de copier nos fichiers actions et les placer dans l'image (qui integre le SDK de rasa), rasa s'occupe du reste en déplyant une API    
**ATTENTION, à premiere vue je ne voit aucune sécurisation de cette API dans le docker-compose...**

Concernant les containers hébergeants le model, ils s'agirais de "rasa-production" et "rasa-worker" qui se connectent de manière sécurisé à l'api de RASA-X pour récuperer la config, ainsi que le model actif. Si vous devez ajouter votre propre model, ou bien permetre d'utiliser un model francais, il faudra ajouter ces instructions dans cette image

## Production
Si on part du principe qu'on utilise un rasa-x par bot il y as 2 éléments :
* La stack rasa-x
* la stack "bot" (rasa-production, rasa-worker, app)

en gros ca veux dire que si on veux faire les choses bien, il faut 2 repository
* 1 repository qui va heberger la config rasa-x (qu'on voit dans le repertoire `rasa-x`)
* 1 repository qui héberge notre bot (le répertoire racine ici présent)

Grace à Rasa-X et a son systeme de récupération depuis un repo git, en soit la seule chose qui n'est pas faite, c'est la mise à jour de notre container `app` (qui contient nos actions).
On peut donc très simplement faire en sorte que :
* Je push mon repository Rasa
* Rasa-X recupere les modifs
* je train(ou j'envoi mon nouveau model) depuis l'interface
* J'active le nouveau model depuis l'interface

pendant ce temps
* Git ci/cd build un nouveau container `app` contenant mon fichier actions.py
* Git ci/cd push ce nouveau container dans la stack rasa-x

### Example de gitlab-ci (je n'ai pas testé mais voila l'idée)
```yaml
stage:
 - build
 - test
 - deploy

# A cette étape on va copier le actions.py de nos sources, dans une image (Dockerfile)
# On envoi ensuite cette image dans le repository gitlab
build_actions:
  stage: build
  service:
    - docker:dind
  script: 
    - docker login -u "$CI_REGISTRY_USER" --password-stdin "$CI_REGISTRY"
    - docker build -t ${CI_REGISTRY_IMAGE}:${$CI_COMMIT_REF_SLUG} .
    - docker push ${CI_REGISTRY_IMAGE}:${$CI_COMMIT_REF_SLUG}

# ici l'idée est de mettre un script pour tester le model
test_my_model:
  stage: test
  image: rasa/rasa-sdk:latest
  script:
    - rasa test
    - # faire un script bash du genre
    - # Si le fichier results/DIETClassifier_errors.json existe, du coup ya erreur

# Dans cette step on télécharge kubeCTL et on va lui demander d'appeler l'api kubernetes pour mettre à jour notre container app
# Pour ca il faut encode son fichier .kube en base64 et le setter en variable d'environement KUBE_CONFIG dans les reglages du repository gitlab(ongler reglages > CI/CD > variables)
deploy_to_production:
    stage: deploy
    image: alpine:3.7
    environment:
      name: production
    only:
      - master
    script:
        - apk update  && apk add --no-cache curl
        - curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
        - chmod +x ./kubectl && mv ./kubectl /usr/local/bin/kubectl
        - mkdir -p $HOME/.kube
        - echo -n $KUBE_CONFIG | base64 -d > $HOME/.kube/config
        - kubectl set image deployment/rasa-x app="${CI_REGISTRY_IMAGE}:${$CI_COMMIT_REF_SLUG}"
```