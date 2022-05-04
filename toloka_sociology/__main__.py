from clean_raw_answers import clean_raw_answers
from process_quality_controls import process_quality_controls
from encode_answers import encode_answers
from postprocess import postprocess

if __name__ == '__main__':
    print('Cleaning data')
    clean_raw_answers('./data/raw_answers', './data/intermediate')
    print('Adding quality controls')
    process_quality_controls('./data/intermediate', './data/processed')
    print('Encoding answers')
    encode_answers('./data/processed', './data/encoded')
    print('Postprocessing')
    postprocess('./data/encoded', './data/final', './data/world_values_survey_extended.xlsx')
    print('Done')