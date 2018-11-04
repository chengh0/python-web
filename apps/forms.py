#!/usr/bin/python
#  -*- coding: utf-8 -*-
from flask_wtf import FlaskForm



class BaseForm(FlaskForm):
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message


    def validate(self):
        return super(BaseForm, self).validate()
