'''
Created on Jul 21, 2018

@author: biya-bi
'''
import base64
import click

from flask import current_app

def get_authentication_header(username, password):
    return {
        'Authorization': 'Basic ' + base64.b64encode(bytes(username + ':' + password, 'ascii')).decode('ascii')
    }
    

def execute_sql_script_file(filename, engine):
    execute_sql_script_files([filename], engine)


def execute_sql_script_files(filenames, engine):
    with engine.begin() as conn:   
        for filename in filenames:
            with current_app.open_resource(filename) as f:
                sqlFile = f.read().decode('utf8')
                sqlCommands = sqlFile.split(';')
            
                for command in sqlCommands:
                    click.echo(command)
                    if command.strip() != '':
                        conn.execute(command)