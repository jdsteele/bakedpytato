#!/usr/bin/env python
from migrate.versioning.shell import main
import cfg
import model

if __name__ == '__main__':
    main(debug='False', repository='sa_migration', url=cfg.sql_url)
