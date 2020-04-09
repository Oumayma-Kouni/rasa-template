FROM rasa/rasa-sdk:latest

# rasa actions
ADD actions /app/actions/

EXPOSE 5055

# the entry point
ENTRYPOINT ["./entrypoint.sh"]
CMD ["start", "--actions", "actions.actions"]