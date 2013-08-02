/*
File: CustomIconRenderer.java ; This file is part of Twister.
Version: 2.001

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
//     ImageIcon port,device,module,testbed;
    ImageIcon device,TB,folder,file;
     
    public CustomIconRenderer() {
//         port = new ImageIcon(RunnerRepository.porticon);
        device = new ImageIcon(RunnerRepository.deviceicon);
        TB = new ImageIcon(RunnerRepository.testbedicon);
        folder = new ImageIcon(RunnerRepository.suitaicon);
        file = new ImageIcon(RunnerRepository.tcicon);
//         module = new ImageIcon(RunnerRepository.moduleicon);
//         testbed = new ImageIcon(RunnerRepository.testbedicon);
    }
     
    public Component getTreeCellRendererComponent(JTree tree,Object value,
                                                 boolean sel,boolean expanded,
                                                 boolean leaf,int row,boolean hasFocus){
        super.getTreeCellRendererComponent(tree, value, sel,expanded, leaf, row, hasFocus);
//         Object nodeObj = ((DefaultMutableTreeNode)value).getUserObject();
//         if (nodeObj instanceof DevicePort) setIcon(port);
//         else if (nodeObj instanceof Device) setIcon(device);
//         else if (nodeObj instanceof DeviceModule) setIcon(module);
//         else if (nodeObj instanceof TestBed) setIcon(testbed);
//         return this;
        Object nodeObj = ((DefaultMutableTreeNode)value).getUserObject();
        if (nodeObj instanceof Node){
            if(((Node)nodeObj).getParent().getParent()==null){
                setIcon(TB);
            } else {
                setIcon(device);
            }
        } else if(nodeObj instanceof MyFolder){
            setIcon(folder);
        } else if(nodeObj instanceof MyParam){
            setIcon(file);
        }
        return this;
    }}
