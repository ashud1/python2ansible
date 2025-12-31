from flask import Flask,render_template,request
import sys
import os 
import subprocess
import yaml
import traceback
import json

# from app_routes import conf


def getParam(dict):
    o_dict={}
    use_dict={}
    g_dict={}
    returnCode=False
    counter=0
    counter2=1
    template={}
    for keys,value in dict.items():
        if keys.startswith("dynamic-textbox"):
            
            returnCode=True
            # print(f"keys {keys} values {value}")
            if keys.startswith("dynamic-textbox-Para"):
                counter=counter+1
                o_dict[keys]={"value":value,"lable":"param "+str(counter)+" : "}
                temp2="div"+str(counter)
                template[temp2]=f"<div>"+f"<label for={ keys }> param " +str(counter)+" : "+f"</label><input type=\"text\" class=\"dynamic-textbox\" id={ keys } name={ keys } value={value}"+">"
                temp=value
                use_dict[value]=""
            elif keys.startswith("dynamic-textbox-Value"):
                template[temp2]=template[temp2]+f"<input type=\"text\" class=\"dynamic-textbox\" id={ keys } name={ keys } value={value}"+">"+"</div>"
                o_dict[keys]={"value":value,"lable":""}
                use_dict[temp]=value
        
    # print(o_dict)
    # print(use_dict)
    # print(template)
    g_dict["returnCode"]=returnCode
    g_dict["html"]=template
    g_dict["ansible"]=use_dict
    return g_dict


def makeTempFile(txt):
    out={"returnCode":"","returnMsg":""}
    try:
        name1=yaml.safe_load(txt)
        file_path = os.path.join(app.root_path,"playbooks", "user-playbook.yml")
        # print(file_path)
        with open(file_path,"w") as file:
            # file.write(txt)
            yaml.dump(name1,file,default_flow_style=False)
            out["returnCode"]=True
            return out
    except yaml.YAMLError as e:
        out["returnCode"]=False
        out["returnMsg"]=e
        return out

def runCmd(checked,ansible):
    out={"returnCode":"","returnMsg":""}
    ansible=json.dumps(ansible)
    if checked:
        file_path = os.path.join(app.root_path, "playbooks", "user-playbook.yml")
        makecmd="ansible-playbook"+" "+file_path+" "+"--extra-vars "+ "\""+str(ansible)+"\""
        #print(makecmd)
        #result=subprocess.run(makecmd,capture_output=True,text=True,shell=True)
        result=subprocess.Popen( makecmd ,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True,text=True)
    else:
        file_path = os.path.join(app.root_path, "playbooks", "master-playbook.yml")
        makecmd="ansible-playbook"+" "+file_path+" "+"--extra-vars "+ "\""+str(ansible)+"\""
        #print(makecmd)
        #result=subprocess.run( makecmd ,capture_output=True,text=True,shell=True)
        result=subprocess.Popen( makecmd ,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True,text=True)

    stdout, stderr = result.communicate()

    #print("Exit code:", result.returncode)
    # print("output:\n", result.stdout)
    # print("Errors:\n", result.stderr)
    #print("output:\n", stdout)
    #print("Errors:\n", stderr)
    if result.returncode==0:
        out["returnCode"]=True
        out["returnMsg"]=stdout
        # return result.stdout 
        return out
    else:
        out["returnCode"]=False
        out["returnMsg"]=stdout+stderr
        # return result.stdout+result.stderr
        return out

app=Flask(__name__)
@app.route("/")
@app.route("/home")
def home():
    # return "Hello, from Flask"+sys.platform
    return render_template("index.html",fields={})

@app.route("/run",methods=["POST","GET"])
def result():
    # return "Hello, from Flask"+sys.platform
    output=request.form.to_dict()
    print(output)
    e=getParam(output)
    #print("###############")
    #print(e)
    html=e["html"]
    ansible=e["ansible"]
    #print(html)
    ansible=e["ansible"]
    #print("****************")
    # print(output)
    if "ibox" in output:
        name=output["ibox"]
        # print(name)
        checked="checkboxHost" in output
        return_dict= makeTempFile(name)
        # print(return_dict)
        err=return_dict["returnCode"]
        out=return_dict["returnMsg"]
        # print(err)
        # print(out)
        #print(f"checked {checked}")
        if err:
            runOutput=runCmd(checked,ansible)
            return render_template("index.html",name=name,validationResult=runOutput["returnMsg"],fields=html,checked=checked)
        else:
            print("Error in yml file")
            return render_template("index.html",name=name,error_desc=out,fields=html,checked=checked)
    else:
        error_desc="Missing Input Box in Post Request"
        return render_template("index.html",name="",error_desc=error_desc,fields=html)


if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)