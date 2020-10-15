from indeed import get_jobs as get_indeed_jobs
from so import get_jobs as get_stack_overflow_jobs
from save import save_to_file

indeed_jobs = get_indeed_jobs()
stackoverflow_jobs = get_stack_overflow_jobs()
jobs = indeed_jobs + stackoverflow_jobs

save_to_file(jobs)