/*
File: SUT.java ; This file is part of Twister.
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
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import javax.swing.tree.DefaultMutableTreeNode;

public class SUT{
    private String name, eps;
    private DefaultMutableTreeNode epsnode;

    public SUT(String name, String eps){
        this.eps = eps;
        this.name=name;
    }
    
     public DefaultMutableTreeNode getEPNode(){
        return epsnode;
    }
    
    public void setEPNode(DefaultMutableTreeNode epsnode){
        this.epsnode = epsnode;
    }
    
   
    public String getEPs(){
        return eps;
    }
    
    public void setEPs(String eps){
        this.eps = eps;
        if(epsnode!=null){
            epsnode.setUserObject("EP: "+eps);
        }
    }
    
    
    public String getName(){
        return name;
    }
    
    public void setName(String name){
        this.name=name;
    }   
    
   
    
    public String toString(){
        return this.name;
    }
}