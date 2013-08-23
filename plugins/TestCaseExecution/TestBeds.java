/*
File: TestBeds.java ; This file is part of Twister.
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
import javax.swing.JTree;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.TreeSelectionModel;
import javax.swing.border.BevelBorder;
import javax.swing.BorderFactory;
import java.awt.BorderLayout;

public class TestBeds extends JPanel{
    private JScrollPane jScrollPane1;
    private JTree tree;
    
    public TestBeds(){
        setLayout(new BorderLayout());
        jScrollPane1 = new JScrollPane();
        add(jScrollPane1,BorderLayout.CENTER);
    }
    
    public void setTree(JTree tree){
        jScrollPane1.setViewportView(tree);
        this.tree = tree;
    }
    
    public JTree getTree(){
        return tree;
    }
}