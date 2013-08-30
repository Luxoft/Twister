/*
File: CustomIconRenderer.java ; This file is part of Twister.
Version: 2.003

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
import javax.swing.tree.DefaultTreeCellRenderer;
import javax.swing.ImageIcon;
import javax.swing.JTree;
import java.awt.Component;
import javax.swing.tree.DefaultMutableTreeNode;

class CustomIconRenderer extends DefaultTreeCellRenderer {
    ImageIcon device,TB,folder,file;
     
    public CustomIconRenderer() {
        device = new ImageIcon(RunnerRepository.deviceicon);
        TB = new ImageIcon(RunnerRepository.testbedicon);
        folder = new ImageIcon(RunnerRepository.suitaicon);
        file = new ImageIcon(RunnerRepository.tcicon);
    }
     
    public Component getTreeCellRendererComponent(JTree tree,Object value,
                                                 boolean sel,boolean expanded,
                                                 boolean leaf,int row,boolean hasFocus){
        super.getTreeCellRendererComponent(tree, value, sel,expanded, leaf, row, hasFocus);
        Object nodeObj = ((DefaultMutableTreeNode)value).getUserObject();
        if (nodeObj instanceof Node){
//             if(((Node)nodeObj).getParent().getParent()==null){
//                 setIcon(TB);
//             } else {
//                 setIcon(device);
//             }
            if(((Node)nodeObj).getType()==0){
                setIcon(TB);
            } else if(((Node)nodeObj).getType()==1){
                setIcon(device);
            }
        } else if(nodeObj instanceof MyFolder){
            setIcon(folder);
        } else if(nodeObj instanceof MyParam){
            setIcon(file);
        }
        return this;
    }}
