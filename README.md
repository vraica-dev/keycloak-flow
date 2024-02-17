# keycloak-flow
Basic Python Keycloak Auth Flow 

# about
This flow is meant to be used between 2 systems, using a service account. 
I've choosed to use OOP and classmethods, in order to cache the ACCESS_TOKEN and REFRESH_TOKEN. This way it wont be necessary to request a new token each time a right is meant in the main client (the one that will actually use the TOKEN received from Keycloak as a Bearer).


# steps to run it localy for testing and dev purposes
1. Run a docker container with Keycloak - check the official doc https://www.keycloak.org/getting-started/getting-started-docker;
2. Via admin page (localhost:8080; default user admin; default pass admin) create the followings:
     1. User  - don't forget to assign pass to it as well as roles;
     2. Client - select the OpenConnect option - Client_ID and Secret key; check the available tabs for setting HS256 as the algo for encode/decode de access token; check the tabs for customizing the exp time;
3. Replace the creds in the py file with yours.
4. Run the file.

