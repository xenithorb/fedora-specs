#!/bin/bash
set -x

get_spec_properties() {
  eval "awk '/^${1~}:/{print \$2}' ../SPECS/*.spec"
}

name="$(get_spec_properties name)"
version="$(get_spec_properties version)"

_libdir=/usr/lib64
_datadir=/usr/share

tar xf pac*.tar.gz
cp -a pac ${name}.orig

# Find and edit use lib strings
mapfile -t FILES_TO_EDIT < <( egrep -lR '^use lib \$RealBin' ./pac )
sed -i "/use lib $RealBin/{s|.*|use lib '${_libdir}/${name}', '${_libdir}/${name}/ex', '${_libdir}/${name}/edit';|}" "${FILES_TO_EDIT[@]}"
unset FILES_TO_EDIT

# Find and edit require strings
mapfile -t FILES_TO_EDIT < <( egrep -lR 'require "\$RealBin' ./pac )
sed -i "/require \"\$RealBin/{s|\$RealBin/lib|${_libdir}/${name}|}" "${FILES_TO_EDIT[@]}"

pushd pac
  find . -type f -exec sed -i \
    -e "s|\$RealBin[ ]*\.[ ]*'/res|'${_datadir}/${name}|g" \
	  -e "s|\$RealBin[ ]*\.[ ]*'/lib|'${_libdir}/${name}|g" \
    '{}' \+
	diff -ru ../${name}.orig . > ../${name}-${version}-libdir.patch
popd
rm -rf pac ${name:-?ERR}.orig
