#!/bin/bash

# Source0 is prepared by
# svn checkout https://svn.code.sf.net/p/netpbm/code/advanced netpbm-%{version}
# svn checkout https://svn.code.sf.net/p/netpbm/code/userguide netpbm-%{version}/userguide
# svn checkout https://svn.code.sf.net/p/netpbm/code/trunk/test netpbm-%{version}/test
# and removing the .svn directories ( find -name "\.svn" -type d -print0 | xargs -0 rm -rf )

VERSION=$1
if [[ -z $VERSION ]]; then
    echo "Version is missing as argument"
    exit 1
fi
NETPBM_NAME="netpbm-$VERSION"
TEMP_DIR="/var/tmp/netpbm"
TARBALL="$TEMP_DIR/$NETPBM_NAME.tar.xz"
mkdir -p $TEMP_DIR
pushd $TEMP_DIR
svn checkout https://svn.code.sf.net/p/netpbm/code/advanced $NETPBM_NAME
svn checkout https://svn.code.sf.net/p/netpbm/code/userguide $NETPBM_NAME/userguide
svn checkout https://svn.code.sf.net/p/netpbm/code/trunk/test $NETPBM_NAME/test
find -name '\.svn' -type d -print0 | xargs -0 rm -rf
tar -cJvf $NETPBM_NAME.tar.xz $NETPBM_NAME
rm -rf $NETPBM_NAME/
popd
if [[ -f "$TARBALL" ]]; then
    cp $TARBALL .
    rm $TARBALL
fi
exit 0
