=================
SaltStack Example
=================

It is used as Salt configuration example in `Slides about SaltStack`_.

Clone this repository and set up VM using Vagrant.

.. code-block:: console

    $ git clone https://github.com/marselester/salt-stack-example.git
    $ cd salt-stack-example/vagrant
    $ vagrant up

In order to interact with VM you should add ``111.222.111.222 salt-hello-world``
to ``/etc/hosts``.

Install Fabric and set up Salt masterless minion in VM.

.. code-block:: console

    $ cd salt-stack-example
    $ pip install fabric
    $ fab setup_masterless_minion

Finally deploy **development** or **production** environment in VM.

.. code-block:: console

    $ fab salt_env:development deploy

Enjoy `the result page`_ (it will be served by Nginx).

.. _Slides about SaltStack: http://marselester.com/saltstack-slides.html
.. _the result page: http://salt-hello-world/
