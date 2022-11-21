# Continuous Integration, Continuous Delivery

The project deployment is as automated as possible to be able to follow the CI/CD principles.

This markdown file describes the architecture of the deployment in depht and elaborates the design decisions behind it.

## Development Stages

At the core, there exist **three stages** for the development `development`, `stage` and `production`.

### Development Stage

The development stage is only for the early development of any changes.
All development changes are only deployed locally by the docker-compose configuration of the `docker-compose.yml`
or `local.docker-compose.yml` file.
The `docker-compose.yml` is for the most interest if the front or backend is changed in some regards.
It does not use any proxy and one can directly interact with the frontend or backend.
On the other hand, the `local.docker-compose.yml` contains the caddy reverse proxy.
This setup is mostly there to configure any proxy settings and test them locally before the deployment.

### Staging Stage

The `staging` environment is automatically deployed if the master branch in the GitHub project is changed.
One can find this stage at [stage.amira3d.io](stage.amira3d.io).
This setup has the purpose to test all changes to the master branch automatically.
The master branch should be deployable all the time.
The staging environment is a little hidden to make sure that only specific persons can validate their changes here.

### Production Stage

If the staging environment has shown no bugs or conflicts in the changes, they can be rolled out in th real production
environment.
The production rollout needs to be triggered manually in the GitHub Project Actions page.
This ensures that the rollout of any changes for the production environment is deliberate.
The production site is at [amira3d.io](amira3d.io).

## GitHub Actions

All automatic deployments are run with GitHub Actions.

## Github Runner Setup

One GitHub Runner is setup on the server.
This enables to deploy on the server directly without any SSH Connection of the runner.
The setup was chosen bc. it seemed like the most convenient solution and transfers the Authentication to the GitHub
team.

For testing and so on, it might be wise to use the hosted runners of GitHub to avoid unnecessary fluctuating CPU load.
For all deployment scripts that should be run on the server, the label `self-hosted `should be used.

### Setup Self-Hosted Github Runner on the Server

The Server currently runs on Ubuntu 20.04.

```
ssh root@159.69.214.39
```

At first, a dedicated user _github-runner_ has to be added without root privileges.
The runner runs in this userspace.
It is mandatory during the github runner setup to have a non-root user which is logical.

1. Add user:

```
adduser github-runner
```

2. Change password:

```
sudo passwd github-runner
```

3. Swith user without root:

```
su - github-runner
```

4. Install the GitHub Runner on your Server
   by [the offcial instruction](https://docs.github.com/en/actions/hosting-your-own-runners/adding-self-hosted-runners).

5. Switch back to root

```
su - root
```

6. Install Docker by [the offcial instruction](https://docs.docker.com/engine/install/ubuntu/).

7. Install Docker Compose by [the offcial instruction](https://docs.docker.com/compose/install/)

8. Add the `docker` group if it doesn't already exist

```
sudo groupadd docker
```

9. Add the connected user $USER to the docker group

```
sudo gpasswd -a github-runner docker
```

10. Log out and log back in so that your group membership is re-evaluatusernameed.

11. Restart the `docker` daemon

```
sudo service docker restart
```

12. Add the new user to the sudo group so that he can execute sudo commands

```
sudo usermod -aG sudo github-runner
```

13. Change back to the github-runner user

```
su - github-runner
```

14. Change into the github-action folder

```
cd actions-runner/
```

15. Make sure the svc.sh file exists (This is the case if the runner is configured)

```
ls

>> bin  config.sh  _diag  env.sh  externals  run-helper.cmd.template  run-helper.sh.template  run.sh  **svc.sh**  _work
``` 

16. [Configuring the self-hosted runner application as a service ](https://docs.github.com/en/actions/hosting-your-own-runners/configuring-the-self-hosted-runner-application-as-a-service)

``` 
sudo ./svc.sh install
``` 

17. Start the service with the following command:

``` 
sudo ./svc.sh start
``` 

18. **Optional:** Checking the status of the service:

``` 
sudo ./svc.sh status
``` 

19. **Optional:** Uninstalling the service:

``` 
sudo ./svc.sh uninstall
``` 