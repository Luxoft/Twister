/*
File: MyParam.java ; This file is part of Twister.
Version: 2.002

Copyright (C) 2012-2013 , Luxoft

Authors: Andrei Costachi <acostachi@luxoft.com>
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
import org.w3c.dom.Node;
class MyParam{
    private Node name,value,description,type;
    
    public void setValue(Node value){
        this.value=value;
    }
    
    public void setDesc(Node description){
        this.description=description;
    }
    
    public void setName(Node name){
        this.name=name;
    }
    
    public void setType(Node type){
        this.type=type;
    }
    
    public Node getType(){
        return type;
    }
    
    public Node getDesc(){
        return description;
    }
    
    public Node getValue(){
        return value;
    }
    
    public Node getName(){
        return name;
    }
    
    public String toString(){
        String n = "";
        String v = "";
        String t = "";
        try{n = name.getNodeValue();
        } catch(Exception e){}
        try{t = type.getNodeValue();
        } catch(Exception e){}
        try{v = value.getNodeValue();
        } catch(Exception e){}
        return n+" : "+v+" : "+t;
    }
}