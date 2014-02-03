/*
File: MyFolder.java ; This file is part of Twister.
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

class MyFolder{
    private Node node,desc;
    private String sut = "";
    private String sutpath = "";
    
    public MyFolder(Node node){
        this.node = node;
    }
    
    public Node getNode(){
        return node;
    }
    
    public void setDesc(Node desc){
        this.desc = desc;
    }
    
    public Node getDesc(){
        return desc;
    }
    
    public void setSut(String sut){
        this.sut = sut;
    }
    
    public String getSut(){
        return sut;
    }
    
    public void setSutPath(String sutpath){
        this.sutpath = sutpath;
    }
    
    public String getSutPath(){
        return sutpath;
    }
    
    public String toString(){
        if(sutpath!=null&&!sutpath.equals("")){
            return node.getNodeValue()+" - "+sutpath;
        }
        return node.getNodeValue();
    }
}
