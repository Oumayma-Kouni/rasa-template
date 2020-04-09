FROM rasa/rasa:1.9.5-full

USER root

# Add custom model (from local path ./my_custom_model)
ADD ./my_custom_model /app/models/fr_my_custom_spacy_model

# Or download spacy FR model
# RUN python -m download fr_core_news_md

# spacy link custom model
RUN python -m spacy link /app/models/fr_my_custom_spacy_model my_custom_model

USER 1001
# the entry point
EXPOSE 5005
ENTRYPOINT ["rasa"]
CMD ["--help"]