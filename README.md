## Script to delete Rocket.Chat Users

### How does this script work?

The script first searches the database for the given username (using the REST API), in order to get the corresponding User ID. After that, this User ID is used to call another API request to delete the user.

### Usage

1. Customize the included `chat.env` file (Make sure that there are no spaces behind the variables)
   * CHAT_HOST: The URL of the chat instance
   * CHAT_ADMIN_USERNAME: The username of an admin account
   * CHAT_ADMIN_PASSWORD: The password of an admin account
   * CHAT_SECURE: Verify SSL Certificates (`True` or `False`)
   * CHAT_CONFIRM_DELETE: Suppress the confirmation to delete the user (should be `True`)
2. Build the docker container: `docker build -t rocketchat-delete-user .`
3. Make the `run.sh` script executable with `chmod +x run.sh`
4. Run the container with the included bash wrapper and pass the username: `./run.sh USER_TO_DELETE`
5. Confirm with `y` or `yes`

