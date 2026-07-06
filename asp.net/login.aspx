<%@ Page Language="VB" AutoEventWireup="false" CodeFile="login.aspx.vb" Inherits="_Default" %>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title></title>
    <style type="text/css">
        .style1
        {
            width: 100%;
            height: 296px;
        }
        .style2
        {
            width: 339px;
        }
        .style3
        {
            width: 339px;
            height: 58px;
        }
        .style4
        {
            height: 58px;
        }
        .style5
        {
            height: 58px;
            width: 405px;
        }
        .style6
        {
            width: 405px;
        }
    </style>
</head>
<body>
    <form id="form1" runat="server">
    <div>
    
        <table class="style1">
            <tr>
                <td class="style3">
                    <asp:Label ID="Label1" runat="server" Text="NAME :"></asp:Label>
                </td>
                <td class="style5">
                    <asp:TextBox ID="TextBox1" runat="server" Width="305px"></asp:TextBox>
                </td>
                <td class="style4">
                    <asp:RequiredFieldValidator ID="RequiredFieldValidator1" runat="server" 
                        ErrorMessage="RequiredFieldValidator"></asp:RequiredFieldValidator>
                </td>
            </tr>
            <tr>
                <td class="style2">
                    <asp:Label ID="Label2" runat="server" Text="AGE :"></asp:Label>
                </td>
                <td class="style6">
                    <asp:TextBox ID="TextBox2" runat="server" Width="306px"></asp:TextBox>
                </td>
                <td>
                    <asp:RangeValidator ID="RangeValidator1" runat="server" 
                        ErrorMessage="RangeValidator"></asp:RangeValidator>
                </td>
            </tr>
            <tr>
                <td class="style2">
                    <asp:Label ID="Label3" runat="server" Text="E - MAIL :"></asp:Label>
                </td>
                <td class="style6">
                    <asp:TextBox ID="TextBox3" runat="server" Width="307px"></asp:TextBox>
                </td>
                <td>
                    <asp:RegularExpressionValidator runat="server" ControlToValidate="TextBox3" 
                        ErrorMessage="RegularExpressionValidator"></asp:RegularExpressionValidator>
                </td>
            </tr>
            <tr>
                <td class="style2">
                    <asp:Label ID="Label4" runat="server" Text="PASSWORD :"></asp:Label>
                </td>
                <td class="style6">
                    <asp:TextBox ID="TextBox4" runat="server" Width="308px"></asp:TextBox>
                </td>
                <td>
                    <asp:RequiredFieldValidator ID="RequiredFieldValidator2" runat="server" 
                        ErrorMessage="RequiredFieldValidator"></asp:RequiredFieldValidator>
                </td>
            </tr>
            <tr>
                <td class="style2">
                    <asp:Label ID="Label5" runat="server" Text="CONFIRM PASSWORD :"></asp:Label>
                </td>
                <td class="style6">
                    <asp:TextBox ID="TextBox5" runat="server" Width="308px"></asp:TextBox>
                </td>
                <td>
                    <asp:CompareValidator ID="CompareValidator1" runat="server" 
                        ErrorMessage="CompareValidator"></asp:CompareValidator>
                </td>
            </tr>
        </table>
    
    </div>
    <p>
        <asp:Button ID="Button1" runat="server" Text="REGISTER" Width="83px" />
    </p>
    </form>
</body>
</html>
