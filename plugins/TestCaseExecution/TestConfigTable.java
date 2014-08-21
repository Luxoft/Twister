/*
File: TestConfigTable.java ; This file is part of Twister.
Version: 3.001

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

import javax.swing.JTable;
import javax.swing.JFrame;
import javax.swing.JCheckBox;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.TableColumnModel;
import javax.swing.JScrollPane;
import java.awt.event.ItemListener;
import java.awt.event.ItemEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseEvent;
import javax.swing.table.TableCellRenderer;
import java.awt.Component;
import javax.swing.table.TableColumn;
import javax.swing.AbstractButton;
import javax.swing.table.JTableHeader;
import javax.swing.UIManager;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import javax.swing.ListSelectionModel;
import javax.swing.event.TableModelEvent;
import javax.swing.event.TableModelListener;


public class TestConfigTable extends JTable{   
    private Object colNames[] = {"Test Configuration File", "Enabled", "Iterator - Only Default", "Iterator - Stop on Fail"};  
    private Object[][] data = {};  
    private DefaultTableModel dtm;  
    private TestConfigManagement tcm;
//     private JTable table;  
    
    public TestConfigTable(TestConfigManagement tcm){
        this.tcm = tcm;
        buildGUI();
    }
  
    public void buildGUI(){
      
        //remove editing on first column on filename
        dtm = new DefaultTableModel(data,colNames){
            public boolean isCellEditable(int row, int col){
                if(col==0)return false;
                return true;}
        };  
        setModel(dtm);
        TableColumn tc = this.getColumnModel().getColumn(1);        
        tc.setCellEditor(this.getDefaultEditor(Boolean.class));  
        tc.setCellRenderer(this.getDefaultRenderer(Boolean.class));  
        
        tc = this.getColumnModel().getColumn(2);  
        tc.setCellEditor(this.getDefaultEditor(Boolean.class));  
        tc.setCellRenderer(this.getDefaultRenderer(Boolean.class));
        
        tc = this.getColumnModel().getColumn(3);  
        tc.setCellEditor(this.getDefaultEditor(Boolean.class));  
        tc.setCellRenderer(this.getDefaultRenderer(Boolean.class));

        dtm.addTableModelListener(new TableModelListener(){
            public void tableChanged(TableModelEvent e){
                if(e.getColumn()>-1&&e.getLastRow()>-1){
                    String filename = (String)dtm.getValueAt(e.getLastRow(), 0);
                    tcm.configModified(filename, Boolean.parseBoolean(dtm.getValueAt(e.getLastRow(), 1).toString()), 
                                                 Boolean.parseBoolean(dtm.getValueAt(e.getLastRow(), 2).toString()),
                                                 Boolean.parseBoolean(dtm.getValueAt(e.getLastRow(), 3).toString()));
                }
            }
        });
        //setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
    }
  
    class MyItemListener implements ItemListener{  
        public int column;
        
        public MyItemListener(int column){
            this.column = column;
        }
        
        public void itemStateChanged(ItemEvent e) {  
            Object source = e.getSource();  
            if (source instanceof AbstractButton == false) return;  
            boolean checked = e.getStateChange() == ItemEvent.SELECTED;  
            for(int x = 0; x < TestConfigTable.this.getRowCount(); x++){  
                TestConfigTable.this.setValueAt(new Boolean(checked),x,column);  
            }  
        }  
    }
  
//     public static void main (String[] args){
//         SwingUtilities.invokeLater(new Runnable(){
//             public void run(){
                
//                 TestConfigTable table = new TestConfigTable(); 
//                 JScrollPane sp = new JScrollPane(table);
//                 JFrame f = new JFrame();  
//                 f.getContentPane().add(sp);  
//                 f.pack();  
//                 f.setLocationRelativeTo(null);  
//                 f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);  
//                 f.setVisible(true); 
//             }  
//         });  
//     }  
}  

class CheckBoxHeader extends JCheckBox implements TableCellRenderer, MouseListener {  
    protected CheckBoxHeader rendererComponent;  
    protected int column;  
    protected boolean mousePressed = false;  
    protected String title;
    
    public CheckBoxHeader(ItemListener itemListener, String title) { 
        this.title = title;
        rendererComponent = this;  
        rendererComponent.addItemListener(itemListener);  
    }  
    
    public Component getTableCellRendererComponent(JTable table, Object value, boolean isSelected, boolean hasFocus, int row, int column) {
        if (table != null) {  
            JTableHeader header = table.getTableHeader();  
            if (header != null) {  
                rendererComponent.setForeground(header.getForeground());  
                rendererComponent.setBackground(header.getBackground());  
                rendererComponent.setFont(header.getFont());  
                header.addMouseListener(rendererComponent);  
            }  
        }  
        setColumn(column);  
        rendererComponent.setText(title);  
        setBorder(UIManager.getBorder("TableHeader.cellBorder"));  
        return rendererComponent;  
    }  
    
    protected void setColumn(int column) {  
        this.column = column;  
    }  
    
    public int getColumn() {  
        return column;  
    }  
    
    protected void handleClickEvent(MouseEvent e) {  
        if (mousePressed) {  
            mousePressed=false;  
            JTableHeader header = (JTableHeader)(e.getSource());  
            JTable tableView = header.getTable();  
            TableColumnModel columnModel = tableView.getColumnModel();  
            int viewColumn = columnModel.getColumnIndexAtX(e.getX());  
            int column = tableView.convertColumnIndexToModel(viewColumn);              
            if (viewColumn == this.column && e.getClickCount() == 1 && column != -1) {  
                doClick();  
            }  
        }  
    }  
    
    public void mouseClicked(MouseEvent e) {  
        handleClickEvent(e);  
        ((JTableHeader)e.getSource()).repaint();  
    }
    
    public void mousePressed(MouseEvent e) {  
        mousePressed = true;  
    }
    
    public void mouseReleased(MouseEvent e) {  
    }
    
    public void mouseEntered(MouseEvent e) {  
    }
    
    public void mouseExited(MouseEvent e) {  
    }  
}  