<h2>CTP Fundmentals</h2>
If you are new to <b>CTP</b>, I would suggest you have a look at this project if you understand Chinese: 

<a>https://github.com/zhuzhenpeng/CTP-TradeServer</a> this project, will give you basic understanding about CTP in a very short period.


If you want to know more about how does the <b>CTP Wrapper source code</b> works, I would recommend you to check this project:
https://github.com/nooperpudd/ctpwrapper This project uses Cython to explain C++ code, then uses Python to wrap them up.


<h2>About This Project</h2>
<br/>
<b>Purpose</b>
This project is a demo about how to make use of the available CTP wrapper. <b>You can consider as the wrapper of ctp wrapper.</b>
I choose this ctp wrapper because it works super good with Python 2.7
https://github.com/lovelylain/pyctp
<br/>
<br/>
Even though there are a lot CTP wrappers on Github, 
few of them demonstrated how to make use of them in the real project. 
They call ReqUserLogin inside OnRspFrontConnection, and call ReqQryTrade inside the OnRspUserLogin. 
While this is definitely not the right way to make use of CTP wrapper. 
In real projects, you should try to decouple all of the different functions rather than one depend on another. 
<br/>
<br/>
<br/>
<b>To run this project, you need the following environment:</b>
<br/>
Linux
<br/>
Python version from 2.5 to 3.4
<br/>
<br/>
<b>Steps to test:</b>
<br/>
1.Check out codes to your local
<br/>
2.Update PyCTPWrapper/ctpwrapper/main.py to add your CTP account and TCP address
<br/>
3.Run PyCTPWrapper/ctpwrapper/main.py
<br/>
<br/>
Codes under ctpwrapper/ctp are built from this project:
https://github.com/lovelylain/pyctp
<br/>
While codes under ctpwrapper/Trade are the demo wrapper class based on the ctpwrapper. 
You can follow this demo class to customise the methods you need. 
<br/>
<br/>
