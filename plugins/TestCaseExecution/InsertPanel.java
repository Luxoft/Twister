/*
File: InsertPanel.java ; This file is part of Twister.
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
import javax.swing.JPanel;
import javax.swing.JFrame;
import javax.swing.JTextField;
import javax.swing.JLabel;
import javax.swing.JButton;
import javax.swing.BorderFactory;
import java.awt.Dimension;
import javax.swing.BoxLayout;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;

class InsertPanel extends JPanel{
    JTextField tsqlstatement;
    
    public InsertPanel(final JPanel parent){
        JLabel id2 = new JLabel();
        tsqlstatement = new JTextField();        
        setBorder(BorderFactory.createEmptyBorder(2, 2, 2, 2));
        setMaximumSize(new Dimension(2000, 25));
        setLayout(new BoxLayout(this, BoxLayout.LINE_AXIS));
        id2.setText("SQL Statement:");
        id2.setBorder(BorderFactory.createEmptyBorder(0, 10, 0, 2));
        add(id2);
        tsqlstatement.setMinimumSize(new Dimension(50, 20));
        add(tsqlstatement); 
        JButton build = new JButton("Build sql");
        build.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                createSQLBuildFrame();
        }});
        add(build);
        JButton jButton3 = new JButton("Remove");
        jButton3.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                parent.remove(InsertPanel.this);
                if(RunnerRepository.window!=null){
                    RunnerRepository.window.mainpanel.p4.revalidate();
                    RunnerRepository.window.mainpanel.p4.repaint();  
                }
            }
        });
        add(jButton3);
    }
    
    public void createSQLBuildFrame(){
        JFrame f = new JFrame();
        f.setTitle("SQL Statement build");
        f.setBounds(100,100,640,480);
        f.setAlwaysOnTop(true);
        f.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        
        
        
        
//         table = new JLabel("Table");
//         query = new JLabel("Resulting query:");
//         jScrollPane1 = new JScrollPane();
//         ttable = new JList();
//         column = new JLabel("Column");
//         jScrollPane2 = new JScrollPane();
//         tcolumn = new JList();
//         values = new JLabel("Values");
//         jButton1 = new JButton();
//         jScrollPane3 = new JScrollPane();
//         tvalues = new JList();
//         queryresult = new JTextField();
// 
// //         ttable.setModel(new AbstractListModel() {
// //             String[] strings = { "Item 1", "Item 2", "Item 3", "Item 4", "Item 5" };
// //             public int getSize() { return strings.length; }
// //             public Object getElementAt(int i) { return strings[i]; }
// //         });
//         jScrollPane1.setViewportView(ttable);
// 
//         tcolumn.setModel(new AbstractListModel() {
//             String[] strings = { "Item 1", "Item 2", "Item 3", "Item 4", "Item 5" };
//             public int getSize() { return strings.length; }
//             public Object getElementAt(int i) { return strings[i]; }
//         });
//         jScrollPane2.setViewportView(tcolumn);
// 
//         values.setText("Values");
// 
//         jButton1.setText("Add");
// 
//         tvalues.setModel(new AbstractListModel() {
//             String[] strings = { "Item 1", "Item 2", "Item 3", "Item 4", "Item 5" };
//             public int getSize() { return strings.length; }
//             public Object getElementAt(int i) { return strings[i]; }
//         });
//         jScrollPane3.setViewportView(tvalues);
// 
//         GroupLayout layout = new GroupLayout(this);
//         this.setLayout(layout);
//         layout.setHorizontalGroup(
//             layout.createParallelGroup(GroupLayout.Alignment.LEADING)
//             .addGroup(GroupLayout.Alignment.CENTER, layout.createSequentialGroup()
//                 .addGap(189, 189, 189)
//                 .addComponent(jButton1)
//                 .addGap(205, 205, 205))
//             .addGroup(layout.createSequentialGroup()
//                 .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
//                     .addGroup(layout.createSequentialGroup()
//                         .addContainerGap()
//                         .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
//                             .addComponent(table)
//                             .addComponent(jScrollPane3))
//                         .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
//                         .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
//                             .addComponent(column)
//                             .addComponent(jScrollPane1))
//                         .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
//                         .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
//                             .addComponent(values)
//                             .addComponent(jScrollPane2)))
//                     .addGroup(layout.createSequentialGroup()
//                         .addGap(10, 10, 10)
//                         .addComponent(query)
//                         .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
//                         .addComponent(queryresult)))
//                 .addContainerGap())
//         );
//         layout.setVerticalGroup(
//             layout.createParallelGroup(GroupLayout.Alignment.LEADING)
//             .addGroup(layout.createSequentialGroup()
//                 .addContainerGap()
//                 .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
//                     .addComponent(table)
//                     .addComponent(column)
//                     .addComponent(values))
//                 .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
//                 .addGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING)
//                     .addComponent(jScrollPane1)
//                     .addComponent(jScrollPane2)
//                     .addComponent(jScrollPane3))
//                 .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
//                 .addGroup(layout.createParallelGroup(GroupLayout.Alignment.BASELINE)
//                     .addComponent(query)
//                     .addComponent(queryresult, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
//                 .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
//                 .addComponent(jButton1)
//                 .addContainerGap())
//         );
        
        
        
        
        f.setVisible(true);
    }
}