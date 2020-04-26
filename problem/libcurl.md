libcurl库
===

##  Error 1 ##

1. Problem

        pycurl: libcurl link-time ssl backend (nss) is different from compile-time ssl backend (openssl)

2. Fix

        pip uninstall pycurl
        export PYCURL_SSL_LIBRARY=nss
        pip install --compile --install-option="--with-nss" --no-cache-dir pycurl

3. More Info

    http://pycurl.io/docs/latest/install.html#ssl


