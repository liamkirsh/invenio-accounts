## $Id$
## CDSware User account information implementation.  Useful for youraccount pages.

## This file is part of the CERN Document Server Software (CDSware).
## Copyright (C) 2002 CERN.
##
## The CDSware is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## The CDSware is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.  
##
## You should have received a copy of the GNU General Public License
## along with CDSware; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

## $Id$
## DO NOT EDIT THIS FILE!  IT WAS AUTOMATICALLY GENERATED FROM CDSware WML SOURCES.

## read config variables:
#include "config.wml"
#include "configbis.wml"

try:
    import sys
    from config import *
    from webpage import page
    import webuser
except ImportError, e:
    print "Error: %s" % e
    import sys
    sys.exit(1)

# perform_display(): display the main features of CDS personalize
def perform_display(req):
    out = ""
    uid = webuser.getUid(req)
    id_user = uid # XXX
    if webuser.isGuestUser(uid):
        id_user=0
    else:
        id_user=1
        

    out += """<P>The CDS Search offers you a possibility to personalize the interface, to set up your own personal library
    of documents, or to set up an automatic alert query that would run periodically and would notify you of search
    results by email.</P>

    <blockquote>
    <dl>

    <dt>
    <A href="./set">Your Settings</A>
    <dd>Set or change your account Email address or password.
    Specify your preferences about the way the interface looks like.
    
    <dt><A href="../youralerts.py/display">Your Searches</A>
    <dd>View all the searches you performed during the last 30 days.

    <dt><A href="../yourbaskets.py/display">Your Baskets</A>
    <dd>With baskets you can define specific collections of items,
    store interesting records you want to access later or share with others."""
    if (id_user == 0):
        out += """<br><FONT color="red"> You are logged in as a <B>guest</B> user, so your baskets
        will disappear at the end of the current session. If you wish you can login or register
        <A href="./login">here</A>.</FONT>"""
    out += """
    <dt><A href="../youralerts.py/list_alerts">Your Alerts</A>
    <dd>Subscribe to a search which will be run periodically by our service.  The result can be sent to you
    via Email or stored in one of your baskets."""
    if (id_user == 0):
        out += """<br><FONT color="red"> You are logged in as a <B>guest</B> user, so your alerts
        will disappear at the end of the current session. If you wish you can login or register
        <A href="./login">here</A>.</FONT>"""

    out += """
    <dt><A href="http://weblib.cern.ch/cgi-bin/checkloan?uid=&version=2">Your Loans</A>
    <dd>Check out book you have on load, submit borrowing requests, etc.  Requires CERN ID."""

    out += """
    </dl>
    </blockquote>"""

    return out

## perform_delete():delete  the account of the user, not implement yet
def perform_delete():
    out = """<p>Deleting your account"""
    return out

## perform_set(email,password): edit your account parameters, email and password.
def perform_set(email,password):

    text = """
        <body>
        <p><big><strong class=headline>Edit account parameters</strong></big>
	<form method="post" action="../youraccount.py/change">
		<p>If you want to change your email address or password, please set new values in the form below.
		<table>
			<tr><td align=right><strong>New email address:</strong><br><small class=important>(mandatory)</small></td><td><input type="text" size="25" name="email" value="%s"><br><small><span class=quicknote>Example:</span> <span class=example>johndoe@example.com</span></small></td><td></td></tr>
			<tr><td align=right><strong>New password:</strong></td><td align=left><input type="password" size="25" name="password" value="%s"><br><small><span class=quicknote>Note:</span> The password phrase may contain punctuation, spaces, etc.</small></td><td><input type="hidden" name="action" value="edit"></td></tr>
			<tr><td align=center colspan=3><code class=blocknote><input class="formbutton" type="submit" value="Set new values"></code>&nbsp;&nbsp;&nbsp;</td></tr>
		</table>
        </form>
      </body>
      """%(email,password)
    return text                    

##  perform_ask(): ask for the user's email and password, for login in the system
def perform_ask():
    text = """
              <p>If you already have an account, please log in by choosing the <strong class=headline>login
              </strong> button below. <br>If you don't own an account yet, please enter the values of your preference and choose the <strong class=headline>register</strong> button.

              <form method="post" action="../youraccount.py/login">


              <table>
                <tr>
		 <td align=right><strong>Email address:</strong><br><small class=important>(mandatory)</small>
		 </td>
                 <td><input type="text" size="25" name="p_email" value="">
			<br><small><span class=quicknote>Example:</span> <span class=example>johndoe@example.com</span></small></td><td></td></tr><tr><td align=right><strong>Password:</strong>
			<br><small class=quicknote>(optional)</small>	
		</td>
		<td align=left><input type="password" size="25" name="p_pw" value="">
			<br><small><span class=quicknote>Note:
					</span> The password phrase may contain punctuation, spaces, etc.
				</small>
		 </td>
                 <td>
		 </td>
                </tr>
                <tr>
		 <td align=center colspan=3><code class=blocknote><input class="formbutton" type="submit" name="action" value="login"></code>&nbsp;&nbsp;&nbsp;<code class=blocknote><input class="formbutton" type="submit" name="action" value="register"></code>&nbsp;&nbsp;&nbsp;
		 </td>
                </tr>
              </table>
              <p><strong>Note:</strong> Your email address will stay strictly confidential and won't be disclosed to any third party. It will be used to indentify you to the CERN Document Server personal services. For example, you may set up an automatic alert search that will look for new preprints and will notify you daily of new arrivals by email.
             </form>
           """
    return text


# perform_logout: display the message of not longer authorized, 
def perform_logout(req):
    out =""
    out+="""    
            <p>You are not longer recognized.  If you wish you can login here <A href="./login">here</A>.
            
         """
    return out

# perform_back(): template for return to a previous page, used for login,register and setting
def perform_back(mess,act):
    out =""
    out+="""
          <body>
             <table>
                <tr>
                  <td align=center>%s
                   <A href="./%s">%s</A></td>
                </tr>
             </table>
            </body>
         """%(mess,act,act)
    
    return out