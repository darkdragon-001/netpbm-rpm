#!/bin/bash

# Source0 is prepared by
# svn checkout https://netpbm.svn.sourceforge.net/svnroot/netpbm/advanced netpbm-%{version}
# svn checkout https://netpbm.svn.sourceforge.net/svnroot/netpbm/userguide netpbm-%{version}/userguide
# svn checkout https://netpbm.svn.sourceforge.net/svnroot/netpbm/trunk/test netpbm-%{version}/test
# and removing the .svn directories ( find -name "\.svn" -type d -print0 | xargs -0 rm -rf )
# and removing the ppmtompeg code, due to patents ( rm -rf netpbm-%{version}/converter/ppm/ppmtompeg/ )

VERSION=$1
if [[ -z $VERSION ]]; then
    echo "Version is missing as argument"
    exit 1
fi
NETPBM_NAME="netpbm-$VERSION"
TEMP_DIR="/var/tmp/netpbm"
TARBALL="$TEMP_DIR/$NETPBM_NAME.tar.gz"
mkdir -p $TEMP_DIR
pushd $TEMP_DIR
svn checkout https://netpbm.svn.sourceforge.net/svnroot/netpbm/advanced $NETPBM_NAME
svn checkout https://netpbm.svn.sourceforge.net/svnroot/netpbm/userguide $NETPBM_NAME/userguide
svn checkout https://netpbm.svn.sourceforge.net/svnroot/netpbm/trunk/test $NETPBM_NAME/test
find -name '\.svn' -type d -print0 | xargs -0 rm -rf
rm -rf $NETPBM_NAME/converter/ppm/ppmtompeg/
tar -czvf $NETPBM_NAME.tar.gz $NETPBM_NAME
rm -rf $NETPBM_NAME/
popd
if [[ -f "$TARBALL" ]]; then
    cp $TARBALL .
    rm $TARBALL
fi
exit 0
