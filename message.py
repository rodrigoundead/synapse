class SynapseMessage():    
    def __init__(self, request, primary_kind="", primary_content=""):
        self.kind = primary_kind
        self.content = primary_content

        if "synapse_msg" in request.session:
            self.kind = request.session["synapse_msg"]["kind"]
            self.content = request.session["synapse_msg"]["content"]
            request.session.pop("synapse_msg")            


def set_message(request, kind, content):
    message = {"kind": f"{kind}"}
    message["content"] = f"{content}"
    request.session["synapse_msg"] = message


def get_message(request, primary_kind="", primary_msg=""):
    return (SynapseMessage(request, primary_kind, primary_msg))
