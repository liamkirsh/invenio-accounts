## $Id$
## CDSware User account information implementation.  Useful for youraccount pages.

## This file is part of the CERN Document Server Software (CDSware).
## Copyright (C) 2002, 2003, 2004, 2005 CERN.
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

import sys
import string
import cgi
from config import *
from webpage import page
from dbquery import run_sql
from webuser import getUid,isGuestUser, get_user_preferences, set_user_preferences
from access_control_admin import acc_findUserRoleActions
from access_control_config import CFG_ACCESS_CONTROL_LEVEL_ACCOUNTS, CFG_EXTERNAL_AUTHENTICATION

imagesurl = "%s/img" % weburl

# perform_info(): display the main features of CDS personalize
def perform_info(req):
    out = ""
    uid = getUid(req)

    out += """<P>The CDS Search offers you a possibility to personalize the interface, to set up your own personal library
    of documents, or to set up an automatic alert query that would run periodically and would notify you of search
    results by email.</P>

    <blockquote>
    <dl>"""

    if not isGuestUser(uid):
        out += """    
               <dt>
               <A href="./edit">Your Settings</A>
               <dd>Set or change your account Email address or password.
               Specify your preferences about the way the interface looks like."""
    
    out += """
    <dt><A href="../youralerts.py/display">Your Searches</A>
    <dd>View all the searches you performed during the last 30 days.
     
    <dt><A href="../yourbaskets.py/display">Your Baskets</A>
    <dd>With baskets you can define specific collections of items,
    store interesting records you want to access later or share with others."""
    if isGuestUser(uid):
        out+= warning_guest_user(type="baskets")
    out += """
    <dt><A href="../youralerts.py/list">Your Alerts</A>
    <dd>Subscribe to a search which will be run periodically by our service.  The result can be sent to you
    via Email or stored in one of your baskets."""
    if isGuestUser(uid):
	 out+= warning_guest_user(type="alerts")
         
    if cfg_cern_site:
        out += """
        <dt><A href="http://weblib.cern.ch/cgi-bin/checkloan?uid=&version=2">Your Loans</A>
        <dd>Check out book you have on load, submit borrowing requests, etc.  Requires CERN ID."""

    out += """
    </dl>
    </blockquote>"""

    return out

def perform_youradminactivities(uid):
    """Return text for the `Your Admin Activities' box.  Analyze
       whether user UID has some admin roles, and if yes, then print
       suitable links for the actions he can do.  If he's not admin,
       print a simple non-authorized message."""
    if isGuestUser(uid):
        return """You seem to be the guest user.  You have to <a href="../youraccount.py/login">login</a> first."""
    out = ""
    your_role_actions = acc_findUserRoleActions(uid)
    your_roles = []
    your_admin_activities = []
    for (role, action) in your_role_actions:
        if role not in your_roles:
            your_roles.append(role)
    if not your_roles:
        out += "<p>You are not authorized to access administrative functions."
    else:
        out += "<p>You seem to be <em>%s</em>. " % string.join(your_roles, ", ")
        out += "Here are some interesting web admin links for you:"
        # add actions found by the RBAC:
        for (role, action) in your_role_actions:
            if action not in your_admin_activities:
                your_admin_activities.append(action)
        # add all actions if user is superadmin, to make sure he'll see all
        # (since it is not necessary for the superadmin to be connected to actions in RBAC tables):
        if "superadmin" in your_roles:
            for action in ["cfgbibformat", "cfgbibrank", "cfgbibindex", "cfgwebaccess", "cfgwebsearch", "cfgwebsubmit"]:
                if action not in your_admin_activities:            
                    your_admin_activities.append(action)
        # print proposed links:
        for action in your_admin_activities:
            if action == "cfgbibformat":
                out += """<br>&nbsp;&nbsp;&nbsp; <a href="%s/admin/bibformat/">Configure BibFormat</a>""" % weburl
            if action == "cfgbibrank":
                out += """<br>&nbsp;&nbsp;&nbsp; <a href="%s/admin/bibrank/bibrankadmin.py">Configure BibRank</a>""" % weburl
            if action == "cfgbibindex":
                out += """<br>&nbsp;&nbsp;&nbsp; <a href="%s/admin/bibindex/bibindexadmin.py">Configure BibIndex</a>""" % weburl
            if action == "cfgwebaccess":
                out += """<br>&nbsp;&nbsp;&nbsp; <a href="%s/admin/webaccess/">Configure WebAccess</a>""" % weburl
            if action == "cfgwebsearch":
                out += """<br>&nbsp;&nbsp;&nbsp; <a href="%s/admin/websearch/websearchadmin.py">Configure WebSearch</a>""" % weburl
            if action == "cfgwebsubmit":
                out += """<br>&nbsp;&nbsp;&nbsp; <a href="%s/admin/websubmit/">Configure WebSubmit</a>""" % weburl
        out += """<br>For more admin-level activities, see the complete <a href="%s/admin/">Admin Area</a>.""" % weburl
    return out
        
# perform_display_account(): display a dynamic page that shows the user's account
def perform_display_account(req,data,bask,aler,sear):
    uid = getUid(req)
    #your account 	
    if isGuestUser(uid):
 	user ="guest"	
	accBody = """You are logged in as guest. You may want to <A href="../youraccount.py/login">login</A> as a regular user <BR><BR>
		  """	
	bask=aler="""The <strong class=headline>guest</strong> users need to <A href="../youraccount.py/login">register</A>&nbspfirst"""
	sear="No queries found"
    else:
 	user = data[0]
        accBody ="""You are logged in as %s. You may want to a) <A href="../youraccount.py/logout">logout</A>; b) edit your <A href="../youraccount.py/edit">account settings</a>.<BR><BR>
		 """%user			
    out =""
    out +=template_account("Your Account",accBody)
    #your baskets
    out +=template_account("Your Baskets",bask)
    out +=template_account("Your Alert Searches",aler)
    out +=template_account("Your Searches",sear)
    out +=template_account("Your Submissions",
                           """You can consult the list of <a href="%s/yoursubmissions.py">your submissions</a>
                              and inquire about their status.""" % weburl)
    out +=template_account("Your Approvals",
                           """You can consult the list of <a href="%s/yourapprovals.py">your approvals</a>
                              with the documents you approved or refereed.""" % weburl)
    out +=template_account("Your Administrative Activities", perform_youradminactivities(uid))
    return out

# template_account() : it is a template for print each of the options from the user's account	
def template_account(title,body):	
    out =""	
    out +="""
	 	      <table class="searchbox" width="90%%" summary=""	>	
                       <thead>
                        <tr>
                         <th class="searchboxheader">%s</th>
                        </tr>		
                       </thead>
                       <tbody>
                        <tr>
                         <td class="searchboxbody">%s</td>
                        </tr>
                       </tbody>
                      </table>""" % (title, body)
    return out 

# warning_guest_user(): It returns an alert message,showing that the user is a guest user and should log into the system
def warning_guest_user(type):

    msg="""You are logged in as a guest user, so your %s will disappear at the end of the current session. If you wish you can
           <a href="../youraccount.py/login">login or register here</a>.
	"""%type
    return """<table class="errorbox" summary="">
                       <thead>
                        <tr>
                         <th class="errorboxheader">%s</th>
                        </tr>
                       </thead>
                      </table>""" % msg
 
## perform_delete():delete  the account of the user, not implement yet
def perform_delete():
    out = """<p>Deleting your account"""
    return out

## perform_set(email,password): edit your account parameters, email and password.
def perform_set(email,password):

    try:
        uid = run_sql("SELECT id FROM user where email=%s", (email,))
        uid = uid[0][0]
    except:
        uid = 0

    CFG_ACCESS_CONTROL_LEVEL_ACCOUNTS_LOCAL = CFG_ACCESS_CONTROL_LEVEL_ACCOUNTS
    prefs = get_user_preferences(uid)
    if CFG_EXTERNAL_AUTHENTICATION.has_key(prefs['login_method']) and  CFG_EXTERNAL_AUTHENTICATION[prefs['login_method']][1] != True:
        CFG_ACCESS_CONTROL_LEVEL_ACCOUNTS_LOCAL = 3

    text = """
        <body>
        <p><big><strong class=headline>Edit parameters</strong></big>
	<form method="post" action="../youraccount.py/change">
		<p>If you want to change your email address or password, please set new values in the form below.
		<table>
			<tr><td align=right><strong>New email address:</strong><br><small class=important>(mandatory)</small></td><td><input type="text" size="25" name="email" %s value="%s"><br><small><span class=quicknote>Example:</span> <span class=example>johndoe@example.com</span></small></td><td></td></tr>
			<tr><td align=right><strong>New password:</strong><br><small class=quicknote>(optional)</small></td><td align=left><input type="password" size="25" name="password" %s value="%s"><br><small><span class=quicknote>Note:</span> The password phrase may contain punctuation, spaces, etc.</small></td></tr><tr><td align=right><strong>Retype password:</strong></td><td align=left><input type="password" size="25" name="password2" %s value="%s"></td><td><input type="hidden" name="action" value="edit"></td></tr>
				<tr><td align=center colspan=3><code class=blocknote><input class="formbutton" type="submit" value="Set new values"></code>&nbsp;&nbsp;&nbsp;</td></tr>
		</table>
        </form>
      </body>	
      """ % (CFG_ACCESS_CONTROL_LEVEL_ACCOUNTS_LOCAL >= 2 and "disabled" or "", email, CFG_ACCESS_CONTROL_LEVEL_ACCOUNTS_LOCAL >= 3 and "disabled" or "",password, CFG_ACCESS_CONTROL_LEVEL_ACCOUNTS_LOCAL >= 3 and "disabled" or "", "")

    if len(CFG_EXTERNAL_AUTHENTICATION) >= 1:
        try:
            uid = run_sql("SELECT id FROM user where email=%s", (email,))
            uid = uid[0][0]
        except:
            uid = 0
        prefs = get_user_preferences(uid)
        current_login_method = prefs['login_method']

        text += """<form method="post" action="../youraccount.py/change">"""
        text += """<big><strong class=headline>Edit login method</strong></big><p>Please select which login method you would like to use to authenticate yourself:<table><tr><td valign=top><b>Select method:</b></td><td>"""
        methods = CFG_EXTERNAL_AUTHENTICATION.keys()
        methods.sort()
        for system in methods:
            text += """<input type="radio" name="login_method" value="%s" %s %s>%s<br>""" % (system, (current_login_method == system and "checked" or ""), CFG_ACCESS_CONTROL_LEVEL_ACCOUNTS >= 4 and "disabled" or "", system)
        text += """</td><td></td></tr><tr><td></td><td><input class="formbutton" type="submit" value="Select method"></td></tr></table></form>"""

    return text                    				

##  create_register_page_box(): register a new account
def create_register_page_box(referer=''):

    text = ""
    if CFG_ACCESS_CONTROL_LEVEL_ACCOUNTS <= 1:
        text += """Please enter your email address and desired password:"""
        if CFG_ACCESS_CONTROL_LEVEL_ACCOUNTS == 1:
            text += "The account will not be possible to use before it has been verified and activated."  
    elif CFG_ACCESS_CONTROL_LEVEL_ACCOUNTS >= 2:
        text += """It is not possible to create an account yourself. Contact <a href="mailto:%s">%s</a> if you want an account.""" % (supportemail, supportemail)
    text += """ 
              <form method="post" action="../youraccount.py/register">
              <input type="hidden" name="referer" value="%s">

              <table>
                <tr>
		 <td align=right><strong>Email address:</strong><br><small class=important>(mandatory)</small>
		 </td>
                 <td><input type="text" size="25" name="p_email" value="">
			<br><small><span class=quicknote>Example:</span> <span class=example>johndoe@example.com</span></small></td>
		 <td></td>
	       </tr>
	       <tr>
		 <td align=right><strong>Password:</strong>	
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
		 <td align=right><strong>Retype Password:</strong>	
		</td>
		<td align=left><input type="password" size="25" name="p_pw2" value="">
		 </td>
                 <td>
		 </td>
                </tr>
                <tr>""" % (cgi.escape(referer))
    if CFG_ACCESS_CONTROL_LEVEL_ACCOUNTS <= 1:
        text += """<td></td><td align=left colspan=3><code class=blocknote><input class="formbutton" type="submit" name="action" value="register"></code></td>"""
    text += """</tr>
              </table>
              <p><strong>Note:</strong> Please do not use valuable passwords such as your Unix, AFS or NICE passwords with this service. Your email address will stay strictly confidential and will not be disclosed to any third party. It will be used to identify you for personal services of %s. For example, you may set up an automatic alert search that will look for new preprints and will notify you daily of new arrivals by email.
           """ % (cdsname)
    return text
	
##  create_login_page_box(): ask for the user's email and password, for login into the system
def create_login_page_box(referer=''):

    text = ""
    text += """
              <p>If you already have an account, please login using the form below. <br>"""
    internal = None
    for system in CFG_EXTERNAL_AUTHENTICATION.keys():
        if not CFG_EXTERNAL_AUTHENTICATION[system][0]:
            internal = system
            break
    if CFG_ACCESS_CONTROL_LEVEL_ACCOUNTS <= 1 and internal:
        text += """If you don't own an account yet, please <a href="./register">register</a> an internal account."""
    else:
        text += """It is not possible to create an account yourself. Contact <a href="mailto:%s">%s</a> if you want an account.""" % (supportemail, supportemail)

    text += """<form method="post" action="../youraccount.py/login">"""
    if len(CFG_EXTERNAL_AUTHENTICATION) > 1: 
        logmethdata = """<select name="login_method">"""
        methods = CFG_EXTERNAL_AUTHENTICATION.keys()
        methods.sort()
        for system in methods:
            logmethdata += """<option value="%s" %s>%s</option>""" % (system, (CFG_EXTERNAL_AUTHENTICATION[system][1]== True and "selected" or ""), system)
        logmethdata += "</select>"
        logmethtitle = """<strong>Login via:</strong>"""
    else:
        for system in CFG_EXTERNAL_AUTHENTICATION.keys():
            logmethdata = """<input type="hidden" name="login_method" value="%s">""" % (system)
            logmethtitle = ""
    text += """
              <table>
              <tr>
		 <td align="right">%s
		 </td>
                 <td>%s</td>
		 <td></td>
	       </tr>
              <tr>
		 <td align="right"><input type="hidden" name="referer" value="%s"><strong>Username:</strong>
		 </td>
                 <td><input type="text" size="25" name="p_email" value=""></td>
		 <td></td>
	       </tr>
	       <tr>
		 <td align="right"><strong>Password:</strong>		
		</td>
		<td align="left"><input type="password" size="25" name="p_pw" value="">
		 </td>
                 <td>
		 </td>
                </tr>
                <tr>
		 <td></td><td align="center" colspan="3"><code class="blocknote"><input class="formbutton" type="submit" name="action" value="login"></code>""" % (logmethtitle, logmethdata, cgi.escape(referer))
    if internal:
        text += """&nbsp;&nbsp;&nbsp;(<a href="./lost">Lost your password?</a>)"""
    text += """
		</td>
		<td>
                </tr>
              </table>"""
    text += "</form>"
    return text


# perform_logout: display the message of not longer authorized, 
def perform_logout(req):
    out =""
    out+="""    
            You are no longer recognized.  If you wish you can <A href="./login">login here</A>.
         """
    return out

#def perform_lost: ask the user for his email, in order to send him the lost password	
def perform_lost():
    out =""
    out +="""
	  <body>
		<form  method="post" action="../youraccount.py/send_email">
      If you have lost password for your CERN Document Server internal
      account, then please enter your email address below and the lost
      password will be emailed to you.<br>
      Note that if you have been using an external login system (such
      as CERN NICE), then we cannot do anything and you have to ask
      there.  Alternatively, you can ask <a href="mailto:%s">%s</a> to change
      your login system from external to internal.<br><br>
		<table>		
	    		<tr>
				<td align=right><strong>Email address:</strong></td>
				<td><input type="text" size="25" name="p_email" value=""></td>
				<td><input type="hidden" name="action" value="lost"></td>
			</tr>
			<tr><td></td>
				<td><code class=blocknote><input class="formbutton" type="submit" value="Send lost password"></code></td>
			</tr>
		</table>
			
		</form>
	  </body>
	  """ % (supportemail, supportemail)
    return out

# perform_emailSent(email): confirm that the password has been emailed to 'email' address
def perform_emailSent(email):

    out =""
    out +="Okay, password has been emailed to %s"%email
    return out

# peform_emailMessage : display a error message when the email introduced is not correct, and sugest to try again
def perform_emailMessage(eMsg):

    out =""
    out +="""
	  <body>
		   %s <A href="../youraccount.py/lost">Try again</A>

          </body>

   	  """%eMsg 
    return out 

# perform_back(): template for return to a previous page, used for login,register and setting 
def perform_back(mess,act,linkname=''): 
    if not linkname:
        linkname = act
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
         """%(mess,act,linkname)
    
    return out
