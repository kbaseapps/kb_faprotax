FROM kbase/sdkbase2:python
MAINTAINER KBase Developer
# -----------------------------------------
WORKDIR /opt

RUN apt-get update && \
apt-get install -y wget zip gcc vim tree

RUN wget https://pages.uoregon.edu/slouca/LoucaLab/archive/FAPROTAX/SECTION_Download/MODULE_Downloads/CLASS_Latest%20release/UNIT_FAPROTAX_1.2.4/FAPROTAX_1.2.4.zip && \ 
unzip FAPROTAX_1.2.4.zip && \ 
rm FAPROTAX_1.2.4.zip

ENV PATH=/opt/FAPROTAX_1.2.4:$PATH

RUN pip install --upgrade pip && \
    pip install pandas \
    numpy==1.19.2 \
    pipenv coverage pytest-cov python-coveralls flake8 \
    dotmap
RUN pip install biom-format


ENV PYTHONUNBUFFERED=True


# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
