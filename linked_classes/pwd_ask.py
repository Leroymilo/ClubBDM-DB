import wx
from wx.lib.embeddedimage import PyEmbeddedImage
from passlib.hash import bcrypt

from gen_classes.pwd_ask import PwdDlg

Key_Png = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAAsTAAALEwEAmpwY'
    b'AAAKU0lEQVRoBe2aaXBV533Gf2e5517p6mqXkARahBYDYsEglhG4SbBZHPBiJ23G6ZdMnHxI'
    b'xp52OvnSTnA77dClkzbJmLgd4oZAxw4uocbU4NQRBBtjBAgkawEhoUW6aNGVdBfp7vec85YZ'
    b'vR80GtJJMxfUzOSZ+c97vun3PHre9yySIoTgd1kqS63fG/gdl84CKYrCo9KxlXnFaoxvZ+Xb'
    b'fxgNMXQ0EPuz5khyBIjxG0oIgc4j1turCvV4VHzJ5RCHap9O1Kx+KcbwOWON/1+dRf1J65XB'
    b'lNUFRPm/uJDDw9abNUU7j9UWXWx+Pkf4TjqEGEaIgfvTj+j6E5f4YW7WzVqHtg3I/E3Z5TH6'
    b'cCt0ZE3xKpHg78obUs9s+EpEK21MojiAWUBIXAfcPWpw8XXH3eOxxLcuJcwWIAKIJavQ4Q0l'
    b'BVpc+YusPPMbG56LZNc/HUPPFhBifjTAiaSB2peTaDq1/MA4fM+0vzlo2TeBCL9eD+83cHhj'
    b'6S6XxpsNT0aq1z4bIavSghAwBwAYEt4hry0AwA0DP3Jw/vv67e/FE9/stew2IPpIK3R4U2ml'
    b'Q1Gad7/qr61+Mg5hmXgS0CW4hBeoDN9Q8d3QcWTalDWmuF84ho46+Phf9DvHo8lXL6SsK8g6'
    b'PZIKWUnth9u/Gqqt3hWHSSAo6+KS4IZM3mkwfKWcjw/6kh3T1mSppjs3NOjF61+JUf2NFEaG'
    b'eMz4nuNIwBYvt1n2dSAMiId6I/v+xhWvVG+OP7fxhTCEAD+gL4SXowFUMPLLUn4+Fr/9T6Ho'
    b'+9/xh/+5s0Pp8l0yIAzLD5h87tVU1auG4/A6Td38oNNJTSv8lhU1OYX2azu/HkIzBASQSS+C'
    b'd0oDSiF2TBVjtj0B3ADOxSxxJjWtQoYCloeyPRZPfc1c/R1Df2Orpm4B3ICSdgOvN5U7VEV5'
    b'4wsv+4vyqlLgAywgY+FmXWxijOoDjcqXM7Q1uaoSqdRVX52qPZ7bYIHDCWv3Q0ED5Qcs9n3b'
    b'XP3nLu3fD2jqLiBLmkjfHojGlT/dtCu8p2p7HPxAQtbGWDiL9oB/hIqmLl44+PXy6iNnDztT'
    b'iVjt58MrVuxJQqoeMiphzWqInKJ4Zwc7LFbM/lg99H7EfhnoBqJpMfCP2yuallcl/3LHV4MQ'
    b'B8KLYOeB5SrHBZQqKPeaeeyZBio2VRWIuVEyimdQXEVQLoNWyyBvPQx1kLHMxtCUEmAdMJo2'
    b'A4rgW4/vnXPf/wEwBqgPSn+RKV0FxQOV2TAzRYY2BrYLjEZYthmcy4F8iIbh9i+wgtB/Quc/'
    b'wvYAkAnoaatQIGk237ng/uOahphi5NkQAfTFlVl4rczDkw9aLhTnQ3EukAfkA9ly8qHjTQhN'
    b'M9yscaaL0Xdtuw0YBmbTton/tm3s9Eet6tuXfpwDSZmPrMzikfASNkeOB8iWq1uuZeDthLu/'
    b'JHQXOi+osZ8I6ybQCdwCwuk8hSL/dnfqtU9aXN1dP8sEGxCABhjSkBsJny3hc5HroskBiiGe'
    b'gBvHsMPQf9bBT0P27SFbfAbcBMYBM50GzGcqc4JOTYtHHTqIBfvADf2tMN63AP5/nYL5aX0L'
    b'Zrx4W1Te7cZ72rKuSfh+IAaQtj3w900r8rW49rPGvbObt740CyqQA7YHhq6AoxXEGgPxWB7K'
    b'orQXXEv4chg8D71nmR2Dtg8dieOpZBvwmZwAINJm4B92VpSrKeXt7c+Fdu74Sgh0IBvsTBj+'
    b'BNw9sKzJCVuKH1CZvAXwpWA6oPsn0HESMwJ95wzembF6R2zRJeFldSAtBg79QUWBaitvPfHl'
    b'4M5tL4RAmeexnND/EeQNQ9F2F2wqAWVhTXKQBuSUQsgHl9+A0U6iAbj9C4Nzner4iWSyBWiT'
    b'1YkDpMXAoc9XLSOhnGx6PvDEthdDIOaZUg4YuABFo5C/RcIjockHIeGVAmmiCLyt8/DhENND'
    b'Ct3vO8V/9YmRH8Xjl4BWmb4fEGkx8De7qstIKe827Q9ubXo+CGKeMWVAfzOU+CG30Qkbli04'
    b'1wvAcsOtK5AQ0PASGC747C3ofg9zTjDQqtN53kgd96W6z8RTLcB14ArgBcy0vJH99VMrl+uW'
    b'8t9PvTjTsGVfENR5xriAwQtQkQD34xmwugRELtjZoJVB3IK2j8A3CSbgKgQyYWaE2QnoOJvB'
    b'r7oU35HZ+PV7pt0hk28DxoBEWt6J/2p3zXIs/nP3H003NO4NgS3v9hYMnYcKE9xbMqFOJt8/'
    b'CoF+KInDSD/4pxlp0wlPKdRvnkbXYaRDo/PDDHFiyOw9EY61mII2Cd8H+Bcn/1tX6LV9tZV2'
    b'Ujn9hf0zGxt3y84XQDgBIxehUgH3JhfUlcz3vM8LEz5IAoGrkIKeXxl8+kFWMhrFDIzGMjPd'
    b'Nm2fOuM/9cXbL0WT14FrEn4EiC3u/G9doYNP16/WFfudPftn1m3fEwANyIfZCEx+CisMyNjo'
    b'gYplkDCgbxSCIe616oz3OKjbFGPwZgbnPnQFj47PXRtLWgNfK8hc71aUvJPB2K3hpNUt+94O'
    b'TAKptH0X+u4X66s1VZx+9ku+9Zs+J5MvgmAAxi9DtQdcFRqUecBywVgIwjGGr+qceycnMeZX'
    b'Ig2FIq/DZ/le94Y+Dlvihux2BCgBHMAgcBcIAhZAWgx8d399vbCV95550bdq25MBsIFC8M+A'
    b'rwVWFoBR4YCkCXEBKcCEnotOms/kJI8OzrbeDMbb13oMx0A0FYhaYgi4KvudAtyACkQWViYN'
    b'BubhFXhv74HpVTt2+0GZhw/OwNRVqC4EvSELDAf0B7j7iYGvTycRU7nanhk9OhC62juXaAFa'
    b'gHsSLgRMAFHSoF97Ch38Yv0qTVU+ePGl8ap122ZBwk/eg7lOWFkG2hoPFJaCN4A1B5cv5tsf'
    b'dCSHA0nT/1nA3zsZN7tk2h1AAACw5aRN+gPg1yqKcvoFCQ/z8BPDELkNK8tBrfdAQT6ETAhG'
    b'iIRUBn2Efz4SuGwJ0S77PAwMAbOLoR+agYMH6uo0ldP7np2sWS/hKYbxAYj1zsMrHhXmkjAx'
    b'ClETTAhNuZiO2OH78EPAZaBHdjoJCIBHYiCVUnbVrI7VbH1C3mHzYLQXbC+srJPfaiIWCW+C'
    b'0ISC3+dgZsLAO5TJaDjpB3zAOBBckr/QJE1RkJ1joqiAB0buAGNQUaNAuRumYkSmFc4cK2Rg'
    b'1EhMzNnhqYgZHAjFRtumI63AIBAGWBIDwlZy3R4TnDDUCVoUyuuAqhxIaRCZo68ri1Pt2siZ'
    b'3rErKVt4gUlgBhgB+oDZJTOgqSLf4zHx9YMRh7KVQEkWZGZDzxSpabja4rGujQe678O3ANeA'
    b'Cdn3sFzNJTPgdInCnIIk7mxwVwIpYDIK3hiYFn09blr6lGlvKH4HaAPa03Wmp8WAQ6fIFUlh'
    b'TcDMkMzSslEswILW1mxxfWy2FxgAvDJx/t8YiCXsnlOnlq1NpixNgIoUCHRUtXvSnrrlC7cD'
    b'd4ApQLDEWvwoUQxsBxqAzEWAiixV34K3JIsl1IOehYwF74AaiwU2MIv8/gyw9AZ+/98qS6v/'
    b'AUoSr1gPNRy7AAAAAElFTkSuQmCC')

# Don't look at that, it's private...
salt = "rbekb5pYmaoMZqufrLNnOu"
hash = "$2b$13$rbekb5pYmaoMZqufrLNnOuScwaz1tOqEAZtpQnLduezlts2EelIhW"
hasher = bcrypt.using(rounds=13, salt=salt)

class Pwd (PwdDlg) :
    def __init__(self, parent):
        super().__init__(parent)
        self.image.SetBitmap(Key_Png.GetBitmap())
    
    def send_pwd(self, event):
        if hasher.verify(self.pwd_ctrl.GetValue(), hash) :
            self.help_txt.SetLabel("Mot de passe correct")
            self.EndModal(1)
            return

        self.help_txt.SetLabel("Mot de passe incorrect")
        self.pwd_ctrl.Clear()
    
    def Close(self, force=False):
        self.EndModal(0)
        return super().Close(force)