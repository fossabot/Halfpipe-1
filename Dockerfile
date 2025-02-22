ARG FMRIPREP_VERSION=20.2.1

FROM nipreps/fmriprep:${FMRIPREP_VERSION}

ENV PATH="/usr/local/miniconda/bin:$PATH" \
    HALFPIPE_RESOURCE_DIR="/home/fmriprep/.cache/halfpipe" \
    TEMPLATEFLOW_HOME="/home/fmriprep/.cache/templateflow"
    
RUN mkdir /ext /halfpipe 

COPY . /halfpipe/

RUN cd /halfpipe && \
    pip install --upgrade pip && \
    pip uninstall --yes fmriprep smriprep mriqc niworkflows nipype statsmodels patsy matplotlib && \
    pip install . && \
    python postsetup.py && \
    rm -rf ~/.cache/pip && \
    cd .. && rm -rf /halfpipe/*
    
ENTRYPOINT ["/usr/local/miniconda/bin/halfpipe"]
