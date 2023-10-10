# Deployment with Ansible


**For deployment to Ubuntu 20.04 LTS machines**

**Assumptions:**
- You have SSH access to this machine set in your `.ssh/config`
- You have registered a domain name for this site and set the DNS to point at your machine's IP address


### Install Ansible

See Ansible docs for more info:
https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html

```sh
sudo apt install ansible
# ~~~ or ~~~
python -m pip install ansible
```

---

### Application configuration

1. Modify the `hosts` file `webserver` block to match your webserver's hostname

1. Create `host_vars/mysite.com.yml` and add a key for your webserver's hostname (replace mysite.com with your actual hostname):
    ```
    hostname: mysite.com
    ```
1. Update the `certbot_renew_email` var in [group_vars/webserver.yml](.group_vars/webserver.yml)

1. Update webapp configuration in [group_vars/webserver.yml](.group_vars/webserver.yml) to suit:
    - Default admin login (please update these for security)
    - `smtp` credentials for your mail server
    - *Optional* - Host installation paths:
        - `project_root` - where this git repository will be cloned
        - `setup_root` - where server configuration will be saved
        - `django_root` - where the application will be served from
        - `venv_root` - where the virtual env will be created

1. Create five variables in the file `group_vars/secrets.yml`:
    - `admin_email`       - login to admin site
    - `admin_password`    - password for above
    - `database_password` - localhost database auth
    - `django_secret_key` - for Django to hash database passwords etc
    - `smtp_password`     - mail server SMTP password (for webforms mail)

1. Encrypt these [Ansible secrets](https://docs.ansible.com/ansible/latest/user_guide/vault.html#encrypting-existing-files) with the ansible vault. Create `~/.ansible.vault.pass` (this is set in [ansible.cfg](./ansible.cfg)) if you don't have one already - it should contain a secure and secret password:
    ```
    ansible-vault encrypt group_vars/secrets.yml
    ```

---

### Run the playbook to deploy

```sh
ansible-playbook -i hosts playbook.yml
```
