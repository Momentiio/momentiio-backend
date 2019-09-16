def def_post_fork(server, worker):
    from psycogreen.gevent import patch_psycopg
    patch_psycopg()
    worker.log.info("Made Psycopg Green")
post_fork = def_post_fork


def def_on_starting(server):
    import subprocess
    subprocess.run(['/usr/local/bin/python', '/code/manage.py', 'collectstatic', '--noinput'], stdout=subprocess.PIPE)
on_starting = def_on_starting
