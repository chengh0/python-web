#!/usr/bin/python
#  -*- coding: utf-8 -*-
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from clbbs import app
from exit import db
from apps.cms import models as cm_models
from apps.front import models as front_models
from apps.models import Banner
from apps.common import models as common_models


CMSUser = cm_models.CMSUser
CMSRole = cm_models.CMSRole
FrontUser = front_models.FrontUser
CMSPermissions = cm_models.CMSPermissions
manager = Manager(app)


Migrate(app,db)
manager.add_command('db',MigrateCommand)


@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_cms_user(username,password,email):
    user = CMSUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()



@manager.option('-t','--telephone',dest='telephone')
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
def create_front_user(telephone,username,password):
    user = FrontUser(telephone=telephone,username=username,password=password)
    db.session.add(user)
    db.session.commit()




@manager.command
def create_role():
    visitor = CMSRole(name='访问者',desc='只能访问相关数据，不能修改')
    visitor.permissions = CMSPermissions.visitor

    operator = CMSRole(name='运维',desc='管理帖子，管理评论，管理前台用户')
    operator.permissions = CMSPermissions.visitor|CMSPermissions.poster|CMSPermissions.frontuser|CMSPermissions.commenter

    admin = CMSRole(name='管理员',desc='拥有所有权限')
    admin.permissions = CMSPermissions.visitor|CMSPermissions.poster|CMSPermissions.commenter|CMSPermissions.boarder|CMSPermissions.frontuser|CMSPermissions.cmsuser

    developer = CMSRole(name = '开发人员',desc = '开发人员专用')
    developer.permissions = CMSPermissions.all_permisssions


    db.session.add_all([visitor,operator,admin,developer])
    db.session.commit()



@manager.option('-e','--email',dest='email')
@manager.option('-n','--name',dest='name')
def add_cmsuser_role(email,name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
        else:
            print('%smeiyouzhegeren'%role)
    else:
        print('%smeiyou'%email)


@manager.command
def text_permisssions():
    user = CMSUser.query.first()
    if user.is_developer:
        print('yongyouquanxian')
    else:
        print('meiyouquanxian')

@manager.command
def create_text_post():
    for i in range(1,50):
        title = '{}biaoti'.format(i)
        content = ':nenrong {}'.format(i)
        board = common_models.Boards.query.first()
        author = front_models.FrontUser.query.first()
        post = common_models.PostModel(title=title,content=content)
        post.board = board
        post.author = author
        db.session.add(post)
        db.session.commit()


if __name__ == '__main__':
    manager.run()