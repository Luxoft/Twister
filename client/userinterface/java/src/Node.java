
/*
File: Node.java ; This file is part of Twister.

Copyright (C) 2012 , Luxoft

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
import java.util.ArrayList;
import java.util.HashMap;

public class Node{
    private String id,name;
    private Path path;
    private HashMap<String,Node> children = new HashMap<String,Node>();
    private HashMap<String,String> properties = new HashMap<String,String>();
    private Node parent;
    private String eps;

    public Node(String id, String path, String name, Node parent,String eps){
        this.eps = eps;
        this.parent = parent;
        this.id = id;
        this.path = new Path(path);
        this.name=name;
    }
    
    public String getEPs(){
        return eps;
    }
    
    public void setEPs(String eps){
        this.eps = eps;
    }
    
    public HashMap<String,Node> getChildren(){
        return children;
    }
    
    public HashMap getProperties(){
        return properties;
    }
    
    public String getID(){
        return id;
    }
    
    public Path getPath(){
        return path;
    }
    
    public String getName(){
        return name;
    }
    public Node getParent(){
        return parent;
    }
    
    public void setParent(Node parent){
        this.parent=parent;
    }
    
    public void setID(String id){
        this.id=id;
    }
    
    public void setPath(String path){
        this.path.setPath(path);
    }
    
    public void setName(String name){
        this.name=name;
    }   
    
    public Node getChild(String id){
        return children.get(id);
    }
    
    public void addChild(String id, Node child){
        children.put(id, child);
    }
    
    public void removeChild(String id){
        children.remove(id);
    }
    
    public String getPropery(String name){
        return properties.get(name);
    }
    
    public void addProperty(String name, String value){
        properties.put(name, value);
    }
    
    public void removeProperty(String name){
        properties.remove(name);
    }
    
    public String toString(){
        return this.name;
    }
}