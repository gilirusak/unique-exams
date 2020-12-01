#!/bin/bash

# fname has prefix ${EXAM_NAME} and suffix soln
EXAM_NAME=cs109_quiz03
OUT_DIR=output

# make output directories
# if they don't already exist
mkdir -p ${OUT_DIR}/tex ${OUT_DIR}/tex_aux ${OUT_DIR}/pdfs_soln

#for i in `seq -f "%04g" 0 $(($1-1))`
for i in 0000 0001 0002 0219 0150 # 0050 0038
do
  # create latex templates
  python3 -m scripts.util.generate_latex ${i} --soln

  # compile latex
  pdflatex -output-directory=${OUT_DIR}/tex_aux -shell-escape ${OUT_DIR}/tex_soln/${EXAM_NAME}_${i}_soln.tex
  pdf_file=${EXAM_NAME}_${i}_soln.pdf
  if [[ -f ${OUT_DIR}/tex_aux/${pdf_file} ]]; then
    if [[ -f ${OUT_DIR}/pdfs_soln/${pdf_file} ]]; then
      cp ${OUT_DIR}/tex_aux/${pdf_file} ${OUT_DIR}/pdfs_soln/${pdf_file} # with prompt, -i
    fi
    cp ${OUT_DIR}/tex_aux/${pdf_file} ${OUT_DIR}/pdfs_soln/${pdf_file}
  fi
done
