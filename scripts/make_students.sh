#!/bin/bash

# fname has prefix ${EXAM_NAME}
EXAM_NAME=cs109_quiz03      # what instructors see
SHORT_EXAM_NAME=quiz03      # what students see
OUT_DIR=output

# make output directories
# if they don't already exist
mkdir -p ${OUT_DIR}/tex ${OUT_DIR}/tex_aux ${OUT_DIR}/pdfs ${OUT_DIR}/zips

for i in `seq -f "%04g" 0 $(($1-1))`
#for i in 0000 0219 0150 0001 0050 0002 0038
do
  # create latex templates
  python3 -m scripts.util.generate_latex ${i}
  python3 -m scripts.util.generate_latex ${i} --template

  # compile latex
  pdflatex -output-directory=${OUT_DIR}/tex_aux -shell-escape ${OUT_DIR}/tex/${EXAM_NAME}_${i}.tex
  pdf_file=${EXAM_NAME}_${i}.pdf
  if [[ -f ${OUT_DIR}/tex_aux/${pdf_file} ]]; then
    if [[ -f ${OUT_DIR}/pdfs/${pdf_file} ]]; then
      cp ${OUT_DIR}/tex_aux/${pdf_file} ${OUT_DIR}/pdfs/${pdf_file} # with prompt, -i
    fi
    cp ${OUT_DIR}/tex_aux/${pdf_file} ${OUT_DIR}/pdfs/${pdf_file}
  fi

  # make zip
  template_file=${EXAM_NAME}_template_${i}.tex
  zip_dirname=${OUT_DIR}/zips/${i}
  zip_file=${i}.zip
  mkdir -p $zip_dirname
  cp ${OUT_DIR}/pdfs/${pdf_file} ${zip_dirname}/${SHORT_EXAM_NAME}.pdf
  cp ${OUT_DIR}/tex_template/${template_file} ${zip_dirname}/${SHORT_EXAM_NAME}_template.tex
  curdir=`pwd`
  cd ${zip_dirname}
  zip ../${zip_file} *
  cd $curdir
  rm -r ${zip_dirname}
done

# finally, make a copy of the unique_rules.csv used
pwd
cp unique_rules.csv "unique_rules.$(date +%Y%m%d%H).csv"
