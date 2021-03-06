import os
import shutil
from fabric import Connection
from invoke import task, run


project_path = '/home/vagrant/sandglass/'
# Local path configuration (can be absolute or relative to fabfile)
deploy_path = 'output'


c = Connection('localhost')


def github(c):
    """
    Add github key to ssh agent

    Usage:
    fab github
    """
    c.run('ssh-add ~/.ssh/github')


@task
def clean(c):
    """
    Remove generated (static) files

    Usage:
    fab clean
    """
    if os.path.isdir(deploy_path):
        shutil.rmtree(deploy_path)
        os.makedirs(deploy_path)


@task
def build(c):
    """
    Build local version of site

    Usage:
    fab biuld
    """
    #c.run('pelican -s pelicanconf.py')
    c.run('python -V')


@task
def rebuild(c):
    """`clean` then `build`"""
    clean(c)
    build(c)


@task
def regenerate(c):
    """Automatically regenerate site upon file modification"""
    c.run('pelican -r -s pelicanconf.py')


############# old fabric1 code

# from fabric.api import *
# import fabric.contrib.project as project
# import os
# import shutil
# import sys
# import SocketServer
#
# from pelican.server import ComplexHTTPRequestHandler
#
# # Local path configuration (can be absolute or relative to fabfile)
# env.deploy_path = 'output'
# DEPLOY_PATH = env.deploy_path
#
# # Remote server configuration
# production = 'root@localhost:22'
# dest_path = '/var/www'
#
# # Rackspace Cloud Files configuration settings
# env.cloudfiles_username = 'my_rackspace_username'
# env.cloudfiles_api_key = 'my_rackspace_api_key'
# env.cloudfiles_container = 'my_cloudfiles_container'
#
# # Github Pages configuration
# env.github_pages_branch = "gh-pages"
#
# # Port for `serve`
# PORT = 8000
#
# def clean():
#     """Remove generated files"""
#     if os.path.isdir(DEPLOY_PATH):
#         shutil.rmtree(DEPLOY_PATH)
#         os.makedirs(DEPLOY_PATH)
#
# def build():
#     """Build local version of site"""
#     local('pelican -s pelicanconf.py')
#
# def rebuild():
#     """`clean` then `build`"""
#     clean()
#     build()
#
# def regenerate():
#     """Automatically regenerate site upon file modification"""
#     local('pelican -r -s pelicanconf.py')
#
# def serve():
#     """Serve site at http://localhost:8000/"""
#     os.chdir(env.deploy_path)
#
#     class AddressReuseTCPServer(SocketServer.TCPServer):
#         allow_reuse_address = True
#
#     server = AddressReuseTCPServer(('', PORT), ComplexHTTPRequestHandler)
#
#     sys.stderr.write('Serving on port {0} ...\n'.format(PORT))
#     server.serve_forever()
#
# def reserve():
#     """`build`, then `serve`"""
#     build()
#     serve()
#
# # def preview():
# #     """Build production version of site"""
# #     local('pelican -s publishconf.py')
#
# def preview():
#     """ Swasher version    """
#     local('cd {} && python -m pelican.server 8092'.format(DEPLOY_PATH))
#
# def cf_upload():
#     """Publish to Rackspace Cloud Files"""
#     rebuild()
#     with lcd(DEPLOY_PATH):
#         local('swift -v -A https://auth.api.rackspacecloud.com/v1.0 '
#               '-U {cloudfiles_username} '
#               '-K {cloudfiles_api_key} '
#               'upload -c {cloudfiles_container} .'.format(**env))
#
# @hosts(production)
# def publish():
#     """Publish to production via rsync"""
#     local('pelican -s publishconf.py')
#     project.rsync_project(
#         remote_dir=dest_path,
#         exclude=".DS_Store",
#         local_dir=DEPLOY_PATH.rstrip('/') + '/',
#         delete=True,
#         extra_opts='-c',
#     )
#
# def netlify_upload():
#     local('cd {} && netlify deploy'.format(DEPLOY_PATH))
#
# def gh_pages():
#     """Publish to GitHub Pages"""
#     rebuild()
#     local("ghp-import -b {github_pages_branch} {deploy_path}".format(**env))
#     local("git push origin {github_pages_branch}".format(**env))
