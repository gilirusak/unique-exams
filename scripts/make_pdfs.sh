#!/bin/bash

# fname has prefix ${EXAM_NAME}
EXAM_NAME=quiz_test
OUT_DIR=output

# make output directories
# if they don't already exist
mkdir -p ${OUT_DIR}/tex ${OUT_DIR}/tex_aux ${OUT_DIR}/pdfs

#for i in `seq -f "%04g" 1 $1`
for i in 0000 #0001 0002 0219 0150 # 0050 0038
do
  python3 -m scripts.util.generate_latex ${i}
  pdflatex -output-directory=${OUT_DIR}/tex_aux -shell-escape ${OUT_DIR}/tex/${EXAM_NAME}_${i}.tex
  pdf_file=${EXAM_NAME}_${i}.pdf
  if [[ -f ${OUT_DIR}/tex_aux/${pdf_file} ]]; then
    if [[ -f ${OUT_DIR}/pdfs/${pdf_file} ]]; then
      cp ${OUT_DIR}/tex_aux/${pdf_file} ${OUT_DIR}/pdfs/${pdf_file} # with prompt, -i
    fi
    cp ${OUT_DIR}/tex_aux/${pdf_file} ${OUT_DIR}/pdfs/${pdf_file}
  fi
done

# finally, make a copy of the unique_rules.csv used
cp unique_rules.csv "unique_rules.$(date +%Y%m%d%H).csv"
