from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators


class LoginForm(FlaskForm):
    '''渲染用户登录HTML表单 Renderizar formulario HTML de inicio de sesión de usuario.'''

    userid = StringField('Cuenta de usuario：', [validators.DataRequired('obligado cuenta de usuario')])
    password = PasswordField('Password：', [validators.DataRequired('obligado password')])


class CustomerRegForm(FlaskForm):
    '''渲染客户注册HTML表单 Renderizar formulario HTML de registro de clientes'''

    userid = StringField('Cuenta de usuario：', [validators.DataRequired('obligado cuente de usuario')])
    name = StringField('Nombre：', [validators.DataRequired('olbigado nombre')])
    password = PasswordField('Password：', [validators.DataRequired('Obligado password')])
    password2 = PasswordField('Confirma password：', [validators.EqualTo('password', message='Las contraseñas ingresadas no coinciden.')])

    # 验证日期的正则表达式 YYYY-MM-DD YY-MM-DD
    reg_date = r'^((((19|20)(([02468][048])|([13579][26]))-02-29))|((20[0-9][0-9])|(19[0-9][0-9]))-((((0[1-9])|(1[0-2]))-((0[1-9])|(1\d)|(2[0-8])))|((((0[13578])|(1[02]))-31)|(((0[1,3-9])|(1[0-2]))-(29|30)))))$'
    birthday = StringField('Fecha de nacimiento：', [validators.Regexp(reg_date, message='La fecha ingresada no es válida')])
    address = StringField('Address：')
    phone = StringField('Phone：')
