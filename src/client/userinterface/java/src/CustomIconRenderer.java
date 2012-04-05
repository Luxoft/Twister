import javax.swing.tree.DefaultTreeCellRenderer;
import javax.swing.ImageIcon;
import javax.swing.JTree;
import java.awt.Component;
import javax.swing.tree.DefaultMutableTreeNode;

class CustomIconRenderer extends DefaultTreeCellRenderer {
    ImageIcon port,device,module,testbed;
     
    public CustomIconRenderer() {
        port = new ImageIcon(Repository.porticon);
        device = new ImageIcon(Repository.deviceicon);
        module = new ImageIcon(Repository.moduleicon);
        testbed = new ImageIcon(Repository.testbedicon);
//         specialIcon = new ImageIcon(CustomIconRenderer.class.getResource("/images/specialIcon.gif"));
    }
     
    public Component getTreeCellRendererComponent(JTree tree,Object value,boolean sel,boolean expanded,boolean leaf,int row,boolean hasFocus){
        super.getTreeCellRendererComponent(tree, value, sel,expanded, leaf, row, hasFocus);
        Object nodeObj = ((DefaultMutableTreeNode)value).getUserObject();
        // check whatever you need to on the node user object
        if (nodeObj instanceof DevicePort) setIcon(port);
        else if (nodeObj instanceof Device) setIcon(device);
        else if (nodeObj instanceof DeviceModule) setIcon(module);
        else if (nodeObj instanceof TestBed) setIcon(testbed);
        return this;}}