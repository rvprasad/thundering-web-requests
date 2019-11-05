#! /usr/bin/env bash

node_timeout=600
for c in `cat reqs-payload-config.txt` ; do
  IFS="," read -a tmp1 <<< $c
  conc_req=${tmp1[0]}
  nums=${tmp1[1]}
  for server in \
      'actix-rust' 'go-server' \
      'nodejs-express-javascript' 'nodejs-javascript' \
      'ktor-kotlin' 'micronaut-kotlin' 'ratpack-kotlin'  'vertx-kotlin' \
      'phoenix_elixir' 'trot_elixir' \
      'cyclone-python' 'flask+uwsgi-python3' 'tornado-python3' \
      'yaws-erlang' 'cowboy-erlang' ; do
    date
    ansible-playbook -i hosts.yml eval-server.yml \
      -e "client=ab server=$server nums=$nums conc_req=$conc_req iter=1 node_timeout=$node_timeout"
    ansible-playbook -i hosts.yml eval-server.yml \
      -e "client=ab server=$server nums=$nums conc_req=$conc_req iter=2 node_timeout=$node_timeout"
    for iter in `seq 1 7` ; do
      date
      ansible-playbook -i hosts.yml eval-server.yml \
        -e "client=wc server=$server nums=$nums conc_req=$conc_req \
        iter=$iter node_timeout=$node_timeout"
    done
  done
done
