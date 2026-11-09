<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="9.6.2">
<drawing>
<settings><setting alwaysvectorfont="no"/><setting verticaltext="up"/></settings>
<grid distance="0.1" unitdist="inch" unit="inch" style="lines" multiple="1" display="no" altdistance="0.01" altunitdist="inch" altunit="inch"/>
<layers>
<layer number="1" name="Top" color="4" fill="1" visible="yes" active="yes"/>
<layer number="16" name="Bottom" color="1" fill="1" visible="yes" active="yes"/>
<layer number="17" name="Pads" color="2" fill="1" visible="yes" active="yes"/>
<layer number="18" name="Vias" color="2" fill="1" visible="yes" active="yes"/>
<layer number="19" name="Unrouted" color="6" fill="1" visible="yes" active="yes"/>
<layer number="20" name="Dimension" color="24" fill="1" visible="yes" active="yes"/>
<layer number="21" name="tPlace" color="7" fill="1" visible="yes" active="yes"/>
<layer number="22" name="bPlace" color="7" fill="1" visible="yes" active="yes"/>
<layer number="23" name="tOrigins" color="15" fill="1" visible="yes" active="yes"/>
<layer number="24" name="bOrigins" color="15" fill="1" visible="yes" active="yes"/>
<layer number="25" name="tNames" color="7" fill="1" visible="yes" active="yes"/>
<layer number="26" name="bNames" color="7" fill="1" visible="yes" active="yes"/>
<layer number="27" name="tValues" color="7" fill="1" visible="yes" active="yes"/>
<layer number="28" name="bValues" color="7" fill="1" visible="yes" active="yes"/>
<layer number="29" name="tStop" color="7" fill="1" visible="yes" active="yes"/>
<layer number="30" name="bStop" color="7" fill="1" visible="yes" active="yes"/>
<layer number="31" name="tCream" color="7" fill="1" visible="yes" active="yes"/>
<layer number="32" name="bCream" color="7" fill="1" visible="yes" active="yes"/>
<layer number="35" name="tGlue" color="7" fill="1" visible="yes" active="yes"/>
<layer number="36" name="bGlue" color="7" fill="1" visible="yes" active="yes"/>
<layer number="39" name="tKeepout" color="4" fill="1" visible="yes" active="yes"/>
<layer number="40" name="bKeepout" color="1" fill="1" visible="yes" active="yes"/>
<layer number="41" name="tRestrict" color="4" fill="1" visible="yes" active="yes"/>
<layer number="42" name="bRestrict" color="1" fill="1" visible="yes" active="yes"/>
<layer number="43" name="vRestrict" color="2" fill="1" visible="yes" active="yes"/>
<layer number="44" name="Drills" color="7" fill="1" visible="yes" active="yes"/>
<layer number="45" name="Holes" color="7" fill="1" visible="yes" active="yes"/>
<layer number="46" name="Milling" color="3" fill="1" visible="yes" active="yes"/>
<layer number="47" name="Measures" color="7" fill="1" visible="yes" active="yes"/>
<layer number="48" name="Document" color="7" fill="1" visible="yes" active="yes"/>
<layer number="49" name="Reference" color="7" fill="1" visible="yes" active="yes"/>
<layer number="51" name="tDocu" color="7" fill="1" visible="yes" active="yes"/>
<layer number="52" name="bDocu" color="7" fill="1" visible="yes" active="yes"/>
<layer number="88" name="SimResults" color="9" fill="1" visible="yes" active="yes"/>
<layer number="89" name="SimProbes" color="9" fill="1" visible="yes" active="yes"/>
<layer number="90" name="Modules" color="5" fill="1" visible="yes" active="yes"/>
<layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes"/>
<layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes"/>
<layer number="93" name="Pins" color="2" fill="1" visible="yes" active="yes"/>
<layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes"/>
<layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes"/>
<layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes"/>
<layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes"/>
<layer number="98" name="Guide" color="6" fill="1" visible="yes" active="yes"/>
</layers>
<schematic xreflabel="%F%N/%S.%C%R" xrefpart="/%S.%C%R">
<description>Dual EV charger controller. Bench-verified netlist, November 2026. Mains nets are in net class "mains" (6 mm to low voltage).</description>
<libraries><library name="evcharger">
<description>Parts for the dual EV charger controller. Footprints for the ESP32 DevKitC and HLK-PM01 follow the SnapEDA parts; check every footprint against the physical part before ordering a PCB.</description>
<packages>
<package name="MODULE_ESP32-DEVKITC"><description>ESP32-DevKitC V4 footprint, 2x19 at 2.54 mm, rows 25.4 mm apart (from SnapEDA part). Measure your board before ordering.</description>
<pad name="1" x="-12.7" y="22.85" drill="1" diameter="1.7" shape="square"/>
<pad name="2" x="-12.7" y="20.31" drill="1" diameter="1.7" shape="round"/>
<pad name="3" x="-12.7" y="17.77" drill="1" diameter="1.7" shape="round"/>
<pad name="4" x="-12.7" y="15.23" drill="1" diameter="1.7" shape="round"/>
<pad name="5" x="-12.7" y="12.69" drill="1" diameter="1.7" shape="round"/>
<pad name="6" x="-12.7" y="10.15" drill="1" diameter="1.7" shape="round"/>
<pad name="7" x="-12.7" y="7.61" drill="1" diameter="1.7" shape="round"/>
<pad name="8" x="-12.7" y="5.07" drill="1" diameter="1.7" shape="round"/>
<pad name="9" x="-12.7" y="2.53" drill="1" diameter="1.7" shape="round"/>
<pad name="10" x="-12.7" y="-0.01" drill="1" diameter="1.7" shape="round"/>
<pad name="11" x="-12.7" y="-2.55" drill="1" diameter="1.7" shape="round"/>
<pad name="12" x="-12.7" y="-5.09" drill="1" diameter="1.7" shape="round"/>
<pad name="13" x="-12.7" y="-7.63" drill="1" diameter="1.7" shape="round"/>
<pad name="14" x="-12.7" y="-10.17" drill="1" diameter="1.7" shape="round"/>
<pad name="15" x="-12.7" y="-12.71" drill="1" diameter="1.7" shape="round"/>
<pad name="16" x="-12.7" y="-15.25" drill="1" diameter="1.7" shape="round"/>
<pad name="17" x="-12.7" y="-17.79" drill="1" diameter="1.7" shape="round"/>
<pad name="18" x="-12.7" y="-20.33" drill="1" diameter="1.7" shape="round"/>
<pad name="19" x="-12.7" y="-22.87" drill="1" diameter="1.7" shape="round"/>
<pad name="20" x="12.7" y="-22.87" drill="1" diameter="1.7" shape="round"/>
<pad name="21" x="12.7" y="-20.33" drill="1" diameter="1.7" shape="round"/>
<pad name="22" x="12.7" y="-17.79" drill="1" diameter="1.7" shape="round"/>
<pad name="23" x="12.7" y="-15.25" drill="1" diameter="1.7" shape="round"/>
<pad name="24" x="12.7" y="-12.71" drill="1" diameter="1.7" shape="round"/>
<pad name="25" x="12.7" y="-10.17" drill="1" diameter="1.7" shape="round"/>
<pad name="26" x="12.7" y="-7.63" drill="1" diameter="1.7" shape="round"/>
<pad name="27" x="12.7" y="-5.09" drill="1" diameter="1.7" shape="round"/>
<pad name="28" x="12.7" y="-2.55" drill="1" diameter="1.7" shape="round"/>
<pad name="29" x="12.7" y="-0.01" drill="1" diameter="1.7" shape="round"/>
<pad name="30" x="12.7" y="2.53" drill="1" diameter="1.7" shape="round"/>
<pad name="31" x="12.7" y="5.07" drill="1" diameter="1.7" shape="round"/>
<pad name="32" x="12.7" y="7.61" drill="1" diameter="1.7" shape="round"/>
<pad name="33" x="12.7" y="10.15" drill="1" diameter="1.7" shape="round"/>
<pad name="34" x="12.7" y="12.69" drill="1" diameter="1.7" shape="round"/>
<pad name="35" x="12.7" y="15.23" drill="1" diameter="1.7" shape="round"/>
<pad name="36" x="12.7" y="17.77" drill="1" diameter="1.7" shape="round"/>
<pad name="37" x="12.7" y="20.31" drill="1" diameter="1.7" shape="round"/>
<pad name="38" x="12.7" y="22.85" drill="1" diameter="1.7" shape="round"/>
<wire x1="-14.2" y1="-27.1" x2="14.2" y2="-27.1" width="0.2032" layer="21"/>
<wire x1="14.2" y1="-27.1" x2="14.2" y2="32.9" width="0.2032" layer="21"/>
<wire x1="14.2" y1="32.9" x2="-14.2" y2="32.9" width="0.2032" layer="21"/>
<wire x1="-14.2" y1="32.9" x2="-14.2" y2="-27.1" width="0.2032" layer="21"/>
<text x="0" y="25.35" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-25.37" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="CONV_HLK-PM01"><description>Hi-Link HLK-PM01, pad positions from SnapEDA part.</description>
<pad name="1" x="-14.7" y="2.5" drill="1.2" diameter="2.2" shape="square"/>
<pad name="2" x="-14.7" y="-2.5" drill="1.2" diameter="2.2" shape="round"/>
<pad name="3" x="14.7" y="7.7" drill="1.2" diameter="2.2" shape="round"/>
<pad name="4" x="14.7" y="-7.7" drill="1.2" diameter="2.2" shape="round"/>
<wire x1="-17" y1="-10.1" x2="17" y2="-10.1" width="0.2032" layer="21"/>
<wire x1="17" y1="-10.1" x2="17" y2="10.1" width="0.2032" layer="21"/>
<wire x1="17" y1="10.1" x2="-17" y2="10.1" width="0.2032" layer="21"/>
<wire x1="-17" y1="10.1" x2="-17" y2="-10.1" width="0.2032" layer="21"/>
<text x="0" y="10.2" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-10.2" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="PINHD-1X3"><description>1x3 pin header, 2.54 mm</description>
<pad name="1" x="-2.54" y="0" drill="1" diameter="1.7" shape="square"/>
<pad name="2" x="0" y="0" drill="1" diameter="1.7" shape="round"/>
<pad name="3" x="2.54" y="0" drill="1" diameter="1.7" shape="round"/>
<wire x1="-3.81" y1="-1.27" x2="3.81" y2="-1.27" width="0.2032" layer="21"/>
<wire x1="3.81" y1="-1.27" x2="3.81" y2="1.27" width="0.2032" layer="21"/>
<wire x1="3.81" y1="1.27" x2="-3.81" y2="1.27" width="0.2032" layer="21"/>
<wire x1="-3.81" y1="1.27" x2="-3.81" y2="-1.27" width="0.2032" layer="21"/>
<text x="0" y="2.5" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-2.5" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="PINHD-1X4"><description>1x4 pin header, 2.54 mm</description>
<pad name="1" x="-3.81" y="0" drill="1" diameter="1.7" shape="square"/>
<pad name="2" x="-1.27" y="0" drill="1" diameter="1.7" shape="round"/>
<pad name="3" x="1.27" y="0" drill="1" diameter="1.7" shape="round"/>
<pad name="4" x="3.81" y="0" drill="1" diameter="1.7" shape="round"/>
<wire x1="-5.08" y1="-1.27" x2="5.08" y2="-1.27" width="0.2032" layer="21"/>
<wire x1="5.08" y1="-1.27" x2="5.08" y2="1.27" width="0.2032" layer="21"/>
<wire x1="5.08" y1="1.27" x2="-5.08" y2="1.27" width="0.2032" layer="21"/>
<wire x1="-5.08" y1="1.27" x2="-5.08" y2="-1.27" width="0.2032" layer="21"/>
<text x="0" y="2.5" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-2.5" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="BSS138-4CH-MODULE"><description>4-channel BSS138 level shifter module, two rows of 6 at 2.54 mm, rows 10.16 mm apart (measure). Order per row: 1, 2, V, GND, 3, 4. Module mounts component side up.</description>
<pad name="1" x="-6.35" y="-5.08" drill="1" diameter="1.7" shape="square"/>
<pad name="2" x="-3.81" y="-5.08" drill="1" diameter="1.7" shape="round"/>
<pad name="3" x="-1.27" y="-5.08" drill="1" diameter="1.7" shape="round"/>
<pad name="4" x="1.27" y="-5.08" drill="1" diameter="1.7" shape="round"/>
<pad name="5" x="3.81" y="-5.08" drill="1" diameter="1.7" shape="round"/>
<pad name="6" x="6.35" y="-5.08" drill="1" diameter="1.7" shape="round"/>
<pad name="7" x="-6.35" y="5.08" drill="1" diameter="1.7" shape="round"/>
<pad name="8" x="-3.81" y="5.08" drill="1" diameter="1.7" shape="round"/>
<pad name="9" x="-1.27" y="5.08" drill="1" diameter="1.7" shape="round"/>
<pad name="10" x="1.27" y="5.08" drill="1" diameter="1.7" shape="round"/>
<pad name="11" x="3.81" y="5.08" drill="1" diameter="1.7" shape="round"/>
<pad name="12" x="6.35" y="5.08" drill="1" diameter="1.7" shape="round"/>
<wire x1="-7.75" y1="-6.7" x2="7.75" y2="-6.7" width="0.2032" layer="21"/>
<wire x1="7.75" y1="-6.7" x2="7.75" y2="6.7" width="0.2032" layer="21"/>
<wire x1="7.75" y1="6.7" x2="-7.75" y2="6.7" width="0.2032" layer="21"/>
<wire x1="-7.75" y1="6.7" x2="-7.75" y2="-6.7" width="0.2032" layer="21"/>
<text x="0" y="7.58" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-7.58" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="TERM-2-5.08"><description>2-way PCB screw terminal, 5.08 mm, rated for mains</description>
<pad name="1" x="-2.54" y="0" drill="1.3" diameter="2.6" shape="square"/>
<pad name="2" x="2.54" y="0" drill="1.3" diameter="2.6" shape="round"/>
<wire x1="-5.08" y1="-3.8" x2="5.08" y2="-3.8" width="0.2032" layer="21"/>
<wire x1="5.08" y1="-3.8" x2="5.08" y2="3.8" width="0.2032" layer="21"/>
<wire x1="5.08" y1="3.8" x2="-5.08" y2="3.8" width="0.2032" layer="21"/>
<wire x1="-5.08" y1="3.8" x2="-5.08" y2="-3.8" width="0.2032" layer="21"/>
<text x="0" y="2.5" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-2.5" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="R-0207-10.16"><description>Axial resistor 0207, 10.16 mm pitch</description>
<pad name="1" x="-5.08" y="0" drill="0.8" diameter="1.6" shape="round"/>
<pad name="2" x="5.08" y="0" drill="0.8" diameter="1.6" shape="round"/>
<wire x1="-3.2" y1="-1" x2="3.2" y2="-1" width="0.2032" layer="21"/>
<wire x1="3.2" y1="-1" x2="3.2" y2="1" width="0.2032" layer="21"/>
<wire x1="3.2" y1="1" x2="-3.2" y2="1" width="0.2032" layer="21"/>
<wire x1="-3.2" y1="1" x2="-3.2" y2="-1" width="0.2032" layer="21"/>
<text x="0" y="2.5" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-2.5" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
<package name="DO-35"><description>DO-35 axial diode, 7.62 mm pitch, band = cathode</description>
<pad name="A" x="-3.81" y="0" drill="0.8" diameter="1.6" shape="round"/>
<pad name="C" x="3.81" y="0" drill="0.8" diameter="1.6" shape="square"/>
<wire x1="-2" y1="-0.9" x2="2" y2="-0.9" width="0.2032" layer="21"/>
<wire x1="2" y1="-0.9" x2="2" y2="0.9" width="0.2032" layer="21"/>
<wire x1="2" y1="0.9" x2="-2" y2="0.9" width="0.2032" layer="21"/>
<wire x1="-2" y1="0.9" x2="-2" y2="-0.9" width="0.2032" layer="21"/>
<wire x1="1.4" y1="-0.9" x2="1.4" y2="0.9" width="0.2032" layer="21"/>
<text x="0" y="2.5" size="1.27" layer="25" align="bottom-center">&gt;NAME</text>
<text x="0" y="-2.5" size="1.27" layer="27" align="top-center">&gt;VALUE</text>
</package>
</packages>
<symbols>
<symbol name="ESP32-DEVKITC">
<wire x1="-10.16" y1="-25.4" x2="10.16" y2="-25.4" width="0.254" layer="94"/>
<wire x1="10.16" y1="-25.4" x2="10.16" y2="25.4" width="0.254" layer="94"/>
<wire x1="10.16" y1="25.4" x2="-10.16" y2="25.4" width="0.254" layer="94"/>
<wire x1="-10.16" y1="25.4" x2="-10.16" y2="-25.4" width="0.254" layer="94"/>
<text x="-10.16" y="26.4" size="1.778" layer="95">&gt;NAME</text>
<text x="-10.16" y="-28" size="1.778" layer="96">&gt;VALUE</text>
<pin name="3V3" x="-15.24" y="22.86" visible="pin" length="middle" direction="pwr" rot="R0"/>
<pin name="EN" x="-15.24" y="20.32" visible="pin" length="middle" direction="io" rot="R0"/>
<pin name="SENSOR_VP" x="-15.24" y="17.78" visible="pin" length="middle" direction="io" rot="R0"/>
<pin name="SENSOR_VN" x="-15.24" y="15.24" visible="pin" length="middle" direction="io" rot="R0"/>
<pin name="IO34" x="-15.24" y="12.7" visible="pin" length="middle" direction="io" rot="R0"/>
<pin name="IO35" x="-15.24" y="10.16" visible="pin" length="middle" direction="io" rot="R0"/>
<pin name="IO32" x="-15.24" y="7.62" visible="pin" length="middle" direction="io" rot="R0"/>
<pin name="IO33" x="-15.24" y="5.08" visible="pin" length="middle" direction="io" rot="R0"/>
<pin name="IO25" x="-15.24" y="2.54" visible="pin" length="middle" direction="io" rot="R0"/>
<pin name="IO26" x="-15.24" y="0" visible="pin" length="middle" direction="io" rot="R0"/>
<pin name="IO27" x="-15.24" y="-2.54" visible="pin" length="middle" direction="io" rot="R0"/>
<pin name="IO14" x="-15.24" y="-5.08" visible="pin" length="middle" direction="io" rot="R0"/>
<pin name="IO12" x="-15.24" y="-7.62" visible="pin" length="middle" direction="io" rot="R0"/>
<pin name="GND1" x="-15.24" y="-10.16" visible="pin" length="middle" direction="pwr" rot="R0"/>
<pin name="IO13" x="-15.24" y="-12.7" visible="pin" length="middle" direction="io" rot="R0"/>
<pin name="SD2" x="-15.24" y="-15.24" visible="pin" length="middle" direction="io" rot="R0"/>
<pin name="SD3" x="-15.24" y="-17.78" visible="pin" length="middle" direction="io" rot="R0"/>
<pin name="CMD" x="-15.24" y="-20.32" visible="pin" length="middle" direction="io" rot="R0"/>
<pin name="EXT_5V" x="-15.24" y="-22.86" visible="pin" length="middle" direction="pwr" rot="R0"/>
<pin name="CLK" x="15.24" y="-22.86" visible="pin" length="middle" direction="io" rot="R180"/>
<pin name="SD0" x="15.24" y="-20.32" visible="pin" length="middle" direction="io" rot="R180"/>
<pin name="SD1" x="15.24" y="-17.78" visible="pin" length="middle" direction="io" rot="R180"/>
<pin name="IO15" x="15.24" y="-15.24" visible="pin" length="middle" direction="io" rot="R180"/>
<pin name="IO2" x="15.24" y="-12.7" visible="pin" length="middle" direction="io" rot="R180"/>
<pin name="IO0" x="15.24" y="-10.16" visible="pin" length="middle" direction="io" rot="R180"/>
<pin name="IO4" x="15.24" y="-7.62" visible="pin" length="middle" direction="io" rot="R180"/>
<pin name="IO16" x="15.24" y="-5.08" visible="pin" length="middle" direction="io" rot="R180"/>
<pin name="IO17" x="15.24" y="-2.54" visible="pin" length="middle" direction="io" rot="R180"/>
<pin name="IO5" x="15.24" y="0" visible="pin" length="middle" direction="io" rot="R180"/>
<pin name="IO18" x="15.24" y="2.54" visible="pin" length="middle" direction="io" rot="R180"/>
<pin name="IO19" x="15.24" y="5.08" visible="pin" length="middle" direction="io" rot="R180"/>
<pin name="GND2" x="15.24" y="7.62" visible="pin" length="middle" direction="pwr" rot="R180"/>
<pin name="IO21" x="15.24" y="10.16" visible="pin" length="middle" direction="io" rot="R180"/>
<pin name="RXD0" x="15.24" y="12.7" visible="pin" length="middle" direction="io" rot="R180"/>
<pin name="TXD0" x="15.24" y="15.24" visible="pin" length="middle" direction="io" rot="R180"/>
<pin name="IO22" x="15.24" y="17.78" visible="pin" length="middle" direction="io" rot="R180"/>
<pin name="IO23" x="15.24" y="20.32" visible="pin" length="middle" direction="io" rot="R180"/>
<pin name="GND3" x="15.24" y="22.86" visible="pin" length="middle" direction="pwr" rot="R180"/>
</symbol>
<symbol name="HLK-PM01">
<wire x1="-7.62" y1="-5.08" x2="7.62" y2="-5.08" width="0.254" layer="94"/>
<wire x1="7.62" y1="-5.08" x2="7.62" y2="5.08" width="0.254" layer="94"/>
<wire x1="7.62" y1="5.08" x2="-7.62" y2="5.08" width="0.254" layer="94"/>
<wire x1="-7.62" y1="5.08" x2="-7.62" y2="-5.08" width="0.254" layer="94"/>
<text x="-7.62" y="6" size="1.778" layer="95">&gt;NAME</text>
<text x="-7.62" y="-7.6" size="1.778" layer="96">&gt;VALUE</text>
<pin name="AC1" x="-12.7" y="2.54" visible="pin" length="middle" direction="pas" rot="R0"/>
<pin name="AC2" x="-12.7" y="-2.54" visible="pin" length="middle" direction="pas" rot="R0"/>
<pin name="+VO" x="12.7" y="2.54" visible="pin" length="middle" direction="pas" rot="R180"/>
<pin name="-VO" x="12.7" y="-2.54" visible="pin" length="middle" direction="pas" rot="R180"/>
</symbol>
<symbol name="PZEM-TTL">
<wire x1="-2.54" y1="-7.62" x2="5.08" y2="-7.62" width="0.254" layer="94"/>
<wire x1="5.08" y1="-7.62" x2="5.08" y2="5.08" width="0.254" layer="94"/>
<wire x1="5.08" y1="5.08" x2="-2.54" y2="5.08" width="0.254" layer="94"/>
<wire x1="-2.54" y1="5.08" x2="-2.54" y2="-7.62" width="0.254" layer="94"/>
<text x="-2.54" y="5.88" size="1.778" layer="95">&gt;NAME</text>
<text x="-2.54" y="-10.22" size="1.778" layer="96">&gt;VALUE</text>
<pin name="VCC" x="-5.08" y="2.54" visible="pin" length="short" direction="pas" rot="R0"/>
<pin name="RX" x="-5.08" y="0" visible="pin" length="short" direction="pas" rot="R0"/>
<pin name="TX" x="-5.08" y="-2.54" visible="pin" length="short" direction="pas" rot="R0"/>
<pin name="GND" x="-5.08" y="-5.08" visible="pin" length="short" direction="pas" rot="R0"/>
</symbol>
<symbol name="RELAY-IN">
<wire x1="-2.54" y1="-5.08" x2="5.08" y2="-5.08" width="0.254" layer="94"/>
<wire x1="5.08" y1="-5.08" x2="5.08" y2="5.08" width="0.254" layer="94"/>
<wire x1="5.08" y1="5.08" x2="-2.54" y2="5.08" width="0.254" layer="94"/>
<wire x1="-2.54" y1="5.08" x2="-2.54" y2="-5.08" width="0.254" layer="94"/>
<text x="-2.54" y="5.88" size="1.778" layer="95">&gt;NAME</text>
<text x="-2.54" y="-7.68" size="1.778" layer="96">&gt;VALUE</text>
<pin name="DC+" x="-5.08" y="2.54" visible="pin" length="short" direction="pas" rot="R0"/>
<pin name="DC-" x="-5.08" y="0" visible="pin" length="short" direction="pas" rot="R0"/>
<pin name="IN" x="-5.08" y="-2.54" visible="pin" length="short" direction="pas" rot="R0"/>
</symbol>
<symbol name="LCD-I2C">
<wire x1="-2.54" y1="-7.62" x2="5.08" y2="-7.62" width="0.254" layer="94"/>
<wire x1="5.08" y1="-7.62" x2="5.08" y2="5.08" width="0.254" layer="94"/>
<wire x1="5.08" y1="5.08" x2="-2.54" y2="5.08" width="0.254" layer="94"/>
<wire x1="-2.54" y1="5.08" x2="-2.54" y2="-7.62" width="0.254" layer="94"/>
<text x="-2.54" y="5.88" size="1.778" layer="95">&gt;NAME</text>
<text x="-2.54" y="-10.22" size="1.778" layer="96">&gt;VALUE</text>
<pin name="GND" x="-5.08" y="2.54" visible="pin" length="short" direction="pas" rot="R0"/>
<pin name="VCC" x="-5.08" y="0" visible="pin" length="short" direction="pas" rot="R0"/>
<pin name="SDA" x="-5.08" y="-2.54" visible="pin" length="short" direction="pas" rot="R0"/>
<pin name="SCL" x="-5.08" y="-5.08" visible="pin" length="short" direction="pas" rot="R0"/>
</symbol>
<symbol name="TOGGLE">
<wire x1="-2.54" y1="-5.08" x2="5.08" y2="-5.08" width="0.254" layer="94"/>
<wire x1="5.08" y1="-5.08" x2="5.08" y2="5.08" width="0.254" layer="94"/>
<wire x1="5.08" y1="5.08" x2="-2.54" y2="5.08" width="0.254" layer="94"/>
<wire x1="-2.54" y1="5.08" x2="-2.54" y2="-5.08" width="0.254" layer="94"/>
<text x="-2.54" y="5.88" size="1.778" layer="95">&gt;NAME</text>
<text x="-2.54" y="-7.68" size="1.778" layer="96">&gt;VALUE</text>
<pin name="GND" x="-5.08" y="2.54" visible="pin" length="short" direction="pas" rot="R0"/>
<pin name="SW1" x="-5.08" y="0" visible="pin" length="short" direction="pas" rot="R0"/>
<pin name="SW2" x="-5.08" y="-2.54" visible="pin" length="short" direction="pas" rot="R0"/>
</symbol>
<symbol name="BSS138-4CH">
<wire x1="-7.62" y1="-10.16" x2="7.62" y2="-10.16" width="0.254" layer="94"/>
<wire x1="7.62" y1="-10.16" x2="7.62" y2="7.62" width="0.254" layer="94"/>
<wire x1="7.62" y1="7.62" x2="-7.62" y2="7.62" width="0.254" layer="94"/>
<wire x1="-7.62" y1="7.62" x2="-7.62" y2="-10.16" width="0.254" layer="94"/>
<text x="-7.62" y="8.6" size="1.778" layer="95">&gt;NAME</text>
<text x="-7.62" y="-12.7" size="1.778" layer="96">&gt;VALUE</text>
<pin name="LV1" x="-12.7" y="5.08" visible="pin" length="middle" direction="pas" rot="R0"/>
<pin name="LV2" x="-12.7" y="2.54" visible="pin" length="middle" direction="pas" rot="R0"/>
<pin name="LV" x="-12.7" y="0" visible="pin" length="middle" direction="pas" rot="R0"/>
<pin name="GND@1" x="-12.7" y="-2.54" visible="pin" length="middle" direction="pas" rot="R0"/>
<pin name="LV3" x="-12.7" y="-5.08" visible="pin" length="middle" direction="pas" rot="R0"/>
<pin name="LV4" x="-12.7" y="-7.62" visible="pin" length="middle" direction="pas" rot="R0"/>
<pin name="HV1" x="12.7" y="5.08" visible="pin" length="middle" direction="pas" rot="R180"/>
<pin name="HV2" x="12.7" y="2.54" visible="pin" length="middle" direction="pas" rot="R180"/>
<pin name="HV" x="12.7" y="0" visible="pin" length="middle" direction="pas" rot="R180"/>
<pin name="GND@2" x="12.7" y="-2.54" visible="pin" length="middle" direction="pas" rot="R180"/>
<pin name="HV3" x="12.7" y="-5.08" visible="pin" length="middle" direction="pas" rot="R180"/>
<pin name="HV4" x="12.7" y="-7.62" visible="pin" length="middle" direction="pas" rot="R180"/>
</symbol>
<symbol name="AC-2">
<wire x1="-2.54" y1="-5.08" x2="5.08" y2="-5.08" width="0.254" layer="94"/>
<wire x1="5.08" y1="-5.08" x2="5.08" y2="2.54" width="0.254" layer="94"/>
<wire x1="5.08" y1="2.54" x2="-2.54" y2="2.54" width="0.254" layer="94"/>
<wire x1="-2.54" y1="2.54" x2="-2.54" y2="-5.08" width="0.254" layer="94"/>
<text x="-2.54" y="3.34" size="1.778" layer="95">&gt;NAME</text>
<text x="-2.54" y="-7.68" size="1.778" layer="96">&gt;VALUE</text>
<pin name="L" x="-5.08" y="0" visible="pin" length="short" direction="pas" rot="R0"/>
<pin name="N" x="-5.08" y="-2.54" visible="pin" length="short" direction="pas" rot="R0"/>
</symbol>
<symbol name="RESISTOR">
<wire x1="-2.54" y1="-1.27" x2="2.54" y2="-1.27" width="0.254" layer="94"/>
<wire x1="2.54" y1="-1.27" x2="2.54" y2="1.27" width="0.254" layer="94"/>
<wire x1="2.54" y1="1.27" x2="-2.54" y2="1.27" width="0.254" layer="94"/>
<wire x1="-2.54" y1="1.27" x2="-2.54" y2="-1.27" width="0.254" layer="94"/>
<text x="-2.54" y="2" size="1.778" layer="95">&gt;NAME</text>
<text x="-2.54" y="-3.6" size="1.778" layer="96">&gt;VALUE</text>
<pin name="1" x="-5.08" y="0" visible="pin" length="short" direction="pas" rot="R0"/>
<pin name="2" x="5.08" y="0" visible="pin" length="short" direction="pas" rot="R180"/>
</symbol>
<symbol name="DIODE">
<wire x1="-1.27" y1="1.27" x2="1.27" y2="0" width="0.254" layer="94"/>
<wire x1="1.27" y1="0" x2="-1.27" y2="-1.27" width="0.254" layer="94"/>
<wire x1="-1.27" y1="-1.27" x2="-1.27" y2="1.27" width="0.254" layer="94"/>
<wire x1="1.27" y1="1.27" x2="1.27" y2="-1.27" width="0.254" layer="94"/>
<wire x1="-2.54" y1="0" x2="-1.27" y2="0" width="0.254" layer="94"/>
<wire x1="1.27" y1="0" x2="2.54" y2="0" width="0.254" layer="94"/>
<text x="-2.54" y="2.2" size="1.778" layer="95">&gt;NAME</text>
<text x="-2.54" y="-3.8" size="1.778" layer="96">&gt;VALUE</text>
<pin name="A" x="-5.08" y="0" visible="pin" length="short" direction="pas" rot="R0"/>
<pin name="C" x="5.08" y="0" visible="pin" length="short" direction="pas" rot="R180"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="ESP32-DEVKITC" prefix="U" uservalue="yes"><description>ESP32-DevKitC V4 (38-pin), incl. WROOM-32U external-antenna variant</description>
<gates><gate name="G$1" symbol="ESP32-DEVKITC" x="0" y="0"/></gates>
<devices><device name="" package="MODULE_ESP32-DEVKITC"><connects>
<connect gate="G$1" pin="3V3" pad="1"/>
<connect gate="G$1" pin="EN" pad="2"/>
<connect gate="G$1" pin="SENSOR_VP" pad="3"/>
<connect gate="G$1" pin="SENSOR_VN" pad="4"/>
<connect gate="G$1" pin="IO34" pad="5"/>
<connect gate="G$1" pin="IO35" pad="6"/>
<connect gate="G$1" pin="IO32" pad="7"/>
<connect gate="G$1" pin="IO33" pad="8"/>
<connect gate="G$1" pin="IO25" pad="9"/>
<connect gate="G$1" pin="IO26" pad="10"/>
<connect gate="G$1" pin="IO27" pad="11"/>
<connect gate="G$1" pin="IO14" pad="12"/>
<connect gate="G$1" pin="IO12" pad="13"/>
<connect gate="G$1" pin="GND1" pad="14"/>
<connect gate="G$1" pin="IO13" pad="15"/>
<connect gate="G$1" pin="SD2" pad="16"/>
<connect gate="G$1" pin="SD3" pad="17"/>
<connect gate="G$1" pin="CMD" pad="18"/>
<connect gate="G$1" pin="EXT_5V" pad="19"/>
<connect gate="G$1" pin="CLK" pad="20"/>
<connect gate="G$1" pin="SD0" pad="21"/>
<connect gate="G$1" pin="SD1" pad="22"/>
<connect gate="G$1" pin="IO15" pad="23"/>
<connect gate="G$1" pin="IO2" pad="24"/>
<connect gate="G$1" pin="IO0" pad="25"/>
<connect gate="G$1" pin="IO4" pad="26"/>
<connect gate="G$1" pin="IO16" pad="27"/>
<connect gate="G$1" pin="IO17" pad="28"/>
<connect gate="G$1" pin="IO5" pad="29"/>
<connect gate="G$1" pin="IO18" pad="30"/>
<connect gate="G$1" pin="IO19" pad="31"/>
<connect gate="G$1" pin="GND2" pad="32"/>
<connect gate="G$1" pin="IO21" pad="33"/>
<connect gate="G$1" pin="RXD0" pad="34"/>
<connect gate="G$1" pin="TXD0" pad="35"/>
<connect gate="G$1" pin="IO22" pad="36"/>
<connect gate="G$1" pin="IO23" pad="37"/>
<connect gate="G$1" pin="GND3" pad="38"/>
</connects><technologies><technology name=""/></technologies></device></devices></deviceset>
<deviceset name="HLK-PM01" prefix="PS" uservalue="yes"><description>Hi-Link HLK-PM01 AC-DC module, 5 V 600 mA</description>
<gates><gate name="G$1" symbol="HLK-PM01" x="0" y="0"/></gates>
<devices><device name="" package="CONV_HLK-PM01"><connects>
<connect gate="G$1" pin="AC1" pad="1"/>
<connect gate="G$1" pin="AC2" pad="2"/>
<connect gate="G$1" pin="-VO" pad="3"/>
<connect gate="G$1" pin="+VO" pad="4"/>
</connects><technologies><technology name=""/></technologies></device></devices></deviceset>
<deviceset name="PZEM-TTL" prefix="J" uservalue="yes"><description>PZEM-004T TTL header: VCC RX TX GND</description>
<gates><gate name="G$1" symbol="PZEM-TTL" x="0" y="0"/></gates>
<devices><device name="" package="PINHD-1X4"><connects>
<connect gate="G$1" pin="VCC" pad="1"/>
<connect gate="G$1" pin="RX" pad="2"/>
<connect gate="G$1" pin="TX" pad="3"/>
<connect gate="G$1" pin="GND" pad="4"/>
</connects><technologies><technology name=""/></technologies></device></devices></deviceset>
<deviceset name="RELAY-IN" prefix="J" uservalue="yes"><description>Relay module control header: DC+ DC- IN</description>
<gates><gate name="G$1" symbol="RELAY-IN" x="0" y="0"/></gates>
<devices><device name="" package="PINHD-1X3"><connects>
<connect gate="G$1" pin="DC+" pad="1"/>
<connect gate="G$1" pin="DC-" pad="2"/>
<connect gate="G$1" pin="IN" pad="3"/>
</connects><technologies><technology name=""/></technologies></device></devices></deviceset>
<deviceset name="LCD-I2C" prefix="J" uservalue="yes"><description>PCF8574 LCD backpack: GND VCC SDA SCL</description>
<gates><gate name="G$1" symbol="LCD-I2C" x="0" y="0"/></gates>
<devices><device name="" package="PINHD-1X4"><connects>
<connect gate="G$1" pin="GND" pad="1"/>
<connect gate="G$1" pin="VCC" pad="2"/>
<connect gate="G$1" pin="SDA" pad="3"/>
<connect gate="G$1" pin="SCL" pad="4"/>
</connects><technologies><technology name=""/></technologies></device></devices></deviceset>
<deviceset name="TOGGLE" prefix="J" uservalue="yes"><description>Panel switches: common GND, car 1, car 2</description>
<gates><gate name="G$1" symbol="TOGGLE" x="0" y="0"/></gates>
<devices><device name="" package="PINHD-1X3"><connects>
<connect gate="G$1" pin="GND" pad="1"/>
<connect gate="G$1" pin="SW1" pad="2"/>
<connect gate="G$1" pin="SW2" pad="3"/>
</connects><technologies><technology name=""/></technologies></device></devices></deviceset>
<deviceset name="BSS138-4CH" prefix="U" uservalue="yes"><description>4-channel BSS138 bidirectional level shifter module (LV1-4 / HV1-4)</description>
<gates><gate name="G$1" symbol="BSS138-4CH" x="0" y="0"/></gates>
<devices><device name="" package="BSS138-4CH-MODULE"><connects>
<connect gate="G$1" pin="LV1" pad="1"/>
<connect gate="G$1" pin="LV2" pad="2"/>
<connect gate="G$1" pin="LV" pad="3"/>
<connect gate="G$1" pin="GND@1" pad="4"/>
<connect gate="G$1" pin="LV3" pad="5"/>
<connect gate="G$1" pin="LV4" pad="6"/>
<connect gate="G$1" pin="HV1" pad="7"/>
<connect gate="G$1" pin="HV2" pad="8"/>
<connect gate="G$1" pin="HV" pad="9"/>
<connect gate="G$1" pin="GND@2" pad="10"/>
<connect gate="G$1" pin="HV3" pad="11"/>
<connect gate="G$1" pin="HV4" pad="12"/>
</connects><technologies><technology name=""/></technologies></device></devices></deviceset>
<deviceset name="AC-2" prefix="J" uservalue="yes"><description>Mains L/N screw terminal</description>
<gates><gate name="G$1" symbol="AC-2" x="0" y="0"/></gates>
<devices><device name="" package="TERM-2-5.08"><connects>
<connect gate="G$1" pin="L" pad="1"/>
<connect gate="G$1" pin="N" pad="2"/>
</connects><technologies><technology name=""/></technologies></device></devices></deviceset>
<deviceset name="RESISTOR" prefix="R" uservalue="yes"><description>Axial resistor</description>
<gates><gate name="G$1" symbol="RESISTOR" x="0" y="0"/></gates>
<devices><device name="" package="R-0207-10.16"><connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects><technologies><technology name=""/></technologies></device></devices></deviceset>
<deviceset name="SCHOTTKY" prefix="D" uservalue="yes"><description>Schottky diode, DO-35 (BAT43 or BAT85)</description>
<gates><gate name="G$1" symbol="DIODE" x="0" y="0"/></gates>
<devices><device name="" package="DO-35"><connects>
<connect gate="G$1" pin="A" pad="A"/>
<connect gate="G$1" pin="C" pad="C"/>
</connects><technologies><technology name=""/></technologies></device></devices></deviceset>
</devicesets>
</library></libraries>
<attributes/><variantdefs/>
<classes><class number="0" name="default" width="0" drill="0"></class><class number="1" name="mains" width="0.6096" drill="0"><clearance class="0" value="6"/><clearance class="1" value="2.5"/></class></classes>
<parts>
<part name="U1" library="evcharger" deviceset="ESP32-DEVKITC" device="" value="ESP32-DEVKITC-32U"/>
<part name="PS1" library="evcharger" deviceset="HLK-PM01" device="" value="HLK-PM01"/>
<part name="J1" library="evcharger" deviceset="AC-2" device="" value="AC-IN"/>
<part name="J5" library="evcharger" deviceset="RELAY-IN" device="" value="RELAY1"/>
<part name="J6" library="evcharger" deviceset="RELAY-IN" device="" value="RELAY2"/>
<part name="J7" library="evcharger" deviceset="TOGGLE" device="" value="TOGGLE"/>
<part name="R1" library="evcharger" deviceset="RESISTOR" device="" value="10k"/>
<part name="D1" library="evcharger" deviceset="SCHOTTKY" device="" value="BAT43"/>
<part name="D2" library="evcharger" deviceset="SCHOTTKY" device="" value="BAT43"/>
<part name="J2" library="evcharger" deviceset="PZEM-TTL" device="" value="PZEM1"/>
<part name="J3" library="evcharger" deviceset="PZEM-TTL" device="" value="PZEM2"/>
<part name="J4" library="evcharger" deviceset="LCD-I2C" device="" value="LCD"/>
<part name="U2" library="evcharger" deviceset="BSS138-4CH" device="" value="BSS138 LEVEL SHIFTER"/>
</parts>
<sheets><sheet><plain>
<text x="20.32" y="190.5" size="3.81" layer="97">DUAL EV CHARGER CONTROLLER</text>
<text x="20.32" y="185.42" size="1.778" layer="97">Mains nets AC_L, AC_N use net class "mains". Feed J1 from the inline 1 A fuse; PZEM voltage leads, relay load wiring and outlets stay off-board.</text>
<text x="20.32" y="182.88" size="1.778" layer="97">PZEM TX diode-OR: cathode (band) toward each PZEM TX, anodes joined at GPIO16 with 10k to 3V3.</text>
</plain><instances>
<instance part="U1" gate="G$1" x="127" y="101.6"/>
<instance part="PS1" gate="G$1" x="101.6" y="160.02"/>
<instance part="J1" gate="G$1" x="25.4" y="170.18"/>
<instance part="J5" gate="G$1" x="50.8" y="124.46"/>
<instance part="J6" gate="G$1" x="50.8" y="104.14"/>
<instance part="J7" gate="G$1" x="50.8" y="83.82"/>
<instance part="R1" gate="G$1" x="180.34" y="116.84"/>
<instance part="D1" gate="G$1" x="180.34" y="101.6"/>
<instance part="D2" gate="G$1" x="180.34" y="88.9"/>
<instance part="J2" gate="G$1" x="33.02" y="50.8"/>
<instance part="J3" gate="G$1" x="71.12" y="50.8"/>
<instance part="J4" gate="G$1" x="109.22" y="50.8"/>
<instance part="U2" gate="G$1" x="165.1" y="50.8"/>
</instances><busses/><nets>
<net name="AC_L" class="1">
<segment>
<pinref part="J1" gate="G$1" pin="L"/>
<wire x1="20.32" y1="170.18" x2="12.7" y2="170.18" width="0.1524" layer="91"/>
<label x="12.7" y="170.18" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="PS1" gate="G$1" pin="AC1"/>
<wire x1="88.9" y1="162.56" x2="81.28" y2="162.56" width="0.1524" layer="91"/>
<label x="81.28" y="162.56" size="1.27" layer="95" rot="R180"/>
</segment>
</net>
<net name="AC_N" class="1">
<segment>
<pinref part="J1" gate="G$1" pin="N"/>
<wire x1="20.32" y1="167.64" x2="12.7" y2="167.64" width="0.1524" layer="91"/>
<label x="12.7" y="167.64" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="PS1" gate="G$1" pin="AC2"/>
<wire x1="88.9" y1="157.48" x2="81.28" y2="157.48" width="0.1524" layer="91"/>
<label x="81.28" y="157.48" size="1.27" layer="95" rot="R180"/>
</segment>
</net>
<net name="+5V" class="0">
<segment>
<pinref part="PS1" gate="G$1" pin="+VO"/>
<wire x1="114.3" y1="162.56" x2="121.92" y2="162.56" width="0.1524" layer="91"/>
<label x="121.92" y="162.56" size="1.27" layer="95" rot="R0"/>
</segment>
<segment>
<pinref part="U1" gate="G$1" pin="EXT_5V"/>
<wire x1="111.76" y1="78.74" x2="104.14" y2="78.74" width="0.1524" layer="91"/>
<label x="104.14" y="78.74" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="J2" gate="G$1" pin="VCC"/>
<wire x1="27.94" y1="53.34" x2="20.32" y2="53.34" width="0.1524" layer="91"/>
<label x="20.32" y="53.34" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="J3" gate="G$1" pin="VCC"/>
<wire x1="66.04" y1="53.34" x2="58.42" y2="53.34" width="0.1524" layer="91"/>
<label x="58.42" y="53.34" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="J4" gate="G$1" pin="VCC"/>
<wire x1="104.14" y1="50.8" x2="96.52" y2="50.8" width="0.1524" layer="91"/>
<label x="96.52" y="50.8" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="J5" gate="G$1" pin="DC+"/>
<wire x1="45.72" y1="127" x2="38.1" y2="127" width="0.1524" layer="91"/>
<label x="38.1" y="127" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="J6" gate="G$1" pin="DC+"/>
<wire x1="45.72" y1="106.68" x2="38.1" y2="106.68" width="0.1524" layer="91"/>
<label x="38.1" y="106.68" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="U2" gate="G$1" pin="HV"/>
<wire x1="177.8" y1="50.8" x2="185.42" y2="50.8" width="0.1524" layer="91"/>
<label x="185.42" y="50.8" size="1.27" layer="95" rot="R0"/>
</segment>
</net>
<net name="GND" class="0">
<segment>
<pinref part="PS1" gate="G$1" pin="-VO"/>
<wire x1="114.3" y1="157.48" x2="121.92" y2="157.48" width="0.1524" layer="91"/>
<label x="121.92" y="157.48" size="1.27" layer="95" rot="R0"/>
</segment>
<segment>
<pinref part="U1" gate="G$1" pin="GND1"/>
<wire x1="111.76" y1="91.44" x2="104.14" y2="91.44" width="0.1524" layer="91"/>
<label x="104.14" y="91.44" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="U1" gate="G$1" pin="GND2"/>
<wire x1="142.24" y1="109.22" x2="149.86" y2="109.22" width="0.1524" layer="91"/>
<label x="149.86" y="109.22" size="1.27" layer="95" rot="R0"/>
</segment>
<segment>
<pinref part="U1" gate="G$1" pin="GND3"/>
<wire x1="142.24" y1="124.46" x2="149.86" y2="124.46" width="0.1524" layer="91"/>
<label x="149.86" y="124.46" size="1.27" layer="95" rot="R0"/>
</segment>
<segment>
<pinref part="J2" gate="G$1" pin="GND"/>
<wire x1="27.94" y1="45.72" x2="20.32" y2="45.72" width="0.1524" layer="91"/>
<label x="20.32" y="45.72" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="J3" gate="G$1" pin="GND"/>
<wire x1="66.04" y1="45.72" x2="58.42" y2="45.72" width="0.1524" layer="91"/>
<label x="58.42" y="45.72" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="J4" gate="G$1" pin="GND"/>
<wire x1="104.14" y1="53.34" x2="96.52" y2="53.34" width="0.1524" layer="91"/>
<label x="96.52" y="53.34" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="J5" gate="G$1" pin="DC-"/>
<wire x1="45.72" y1="124.46" x2="38.1" y2="124.46" width="0.1524" layer="91"/>
<label x="38.1" y="124.46" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="J6" gate="G$1" pin="DC-"/>
<wire x1="45.72" y1="104.14" x2="38.1" y2="104.14" width="0.1524" layer="91"/>
<label x="38.1" y="104.14" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="J7" gate="G$1" pin="GND"/>
<wire x1="45.72" y1="86.36" x2="38.1" y2="86.36" width="0.1524" layer="91"/>
<label x="38.1" y="86.36" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="U2" gate="G$1" pin="GND@1"/>
<wire x1="152.4" y1="48.26" x2="144.78" y2="48.26" width="0.1524" layer="91"/>
<label x="144.78" y="48.26" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="U2" gate="G$1" pin="GND@2"/>
<wire x1="177.8" y1="48.26" x2="185.42" y2="48.26" width="0.1524" layer="91"/>
<label x="185.42" y="48.26" size="1.27" layer="95" rot="R0"/>
</segment>
</net>
<net name="+3V3" class="0">
<segment>
<pinref part="U1" gate="G$1" pin="3V3"/>
<wire x1="111.76" y1="124.46" x2="104.14" y2="124.46" width="0.1524" layer="91"/>
<label x="104.14" y="124.46" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="R1" gate="G$1" pin="1"/>
<wire x1="175.26" y1="116.84" x2="167.64" y2="116.84" width="0.1524" layer="91"/>
<label x="167.64" y="116.84" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="U2" gate="G$1" pin="LV"/>
<wire x1="152.4" y1="50.8" x2="144.78" y2="50.8" width="0.1524" layer="91"/>
<label x="144.78" y="50.8" size="1.27" layer="95" rot="R180"/>
</segment>
</net>
<net name="PZEM_TX" class="0">
<segment>
<pinref part="U1" gate="G$1" pin="IO16"/>
<wire x1="142.24" y1="96.52" x2="149.86" y2="96.52" width="0.1524" layer="91"/>
<label x="149.86" y="96.52" size="1.27" layer="95" rot="R0"/>
</segment>
<segment>
<pinref part="D1" gate="G$1" pin="A"/>
<wire x1="175.26" y1="101.6" x2="167.64" y2="101.6" width="0.1524" layer="91"/>
<label x="167.64" y="101.6" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="D2" gate="G$1" pin="A"/>
<wire x1="175.26" y1="88.9" x2="167.64" y2="88.9" width="0.1524" layer="91"/>
<label x="167.64" y="88.9" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="R1" gate="G$1" pin="2"/>
<wire x1="185.42" y1="116.84" x2="193.04" y2="116.84" width="0.1524" layer="91"/>
<label x="193.04" y="116.84" size="1.27" layer="95" rot="R0"/>
</segment>
</net>
<net name="PZEM1_TX" class="0">
<segment>
<pinref part="J2" gate="G$1" pin="TX"/>
<wire x1="27.94" y1="48.26" x2="20.32" y2="48.26" width="0.1524" layer="91"/>
<label x="20.32" y="48.26" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="D1" gate="G$1" pin="C"/>
<wire x1="185.42" y1="101.6" x2="193.04" y2="101.6" width="0.1524" layer="91"/>
<label x="193.04" y="101.6" size="1.27" layer="95" rot="R0"/>
</segment>
</net>
<net name="PZEM2_TX" class="0">
<segment>
<pinref part="J3" gate="G$1" pin="TX"/>
<wire x1="66.04" y1="48.26" x2="58.42" y2="48.26" width="0.1524" layer="91"/>
<label x="58.42" y="48.26" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="D2" gate="G$1" pin="C"/>
<wire x1="185.42" y1="88.9" x2="193.04" y2="88.9" width="0.1524" layer="91"/>
<label x="193.04" y="88.9" size="1.27" layer="95" rot="R0"/>
</segment>
</net>
<net name="PZEM_RX" class="0">
<segment>
<pinref part="U1" gate="G$1" pin="IO17"/>
<wire x1="142.24" y1="99.06" x2="149.86" y2="99.06" width="0.1524" layer="91"/>
<label x="149.86" y="99.06" size="1.27" layer="95" rot="R0"/>
</segment>
<segment>
<pinref part="J2" gate="G$1" pin="RX"/>
<wire x1="27.94" y1="50.8" x2="20.32" y2="50.8" width="0.1524" layer="91"/>
<label x="20.32" y="50.8" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="J3" gate="G$1" pin="RX"/>
<wire x1="66.04" y1="50.8" x2="58.42" y2="50.8" width="0.1524" layer="91"/>
<label x="58.42" y="50.8" size="1.27" layer="95" rot="R180"/>
</segment>
</net>
<net name="RELAY1" class="0">
<segment>
<pinref part="U1" gate="G$1" pin="IO25"/>
<wire x1="111.76" y1="104.14" x2="104.14" y2="104.14" width="0.1524" layer="91"/>
<label x="104.14" y="104.14" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="J5" gate="G$1" pin="IN"/>
<wire x1="45.72" y1="121.92" x2="38.1" y2="121.92" width="0.1524" layer="91"/>
<label x="38.1" y="121.92" size="1.27" layer="95" rot="R180"/>
</segment>
</net>
<net name="RELAY2" class="0">
<segment>
<pinref part="U1" gate="G$1" pin="IO26"/>
<wire x1="111.76" y1="101.6" x2="104.14" y2="101.6" width="0.1524" layer="91"/>
<label x="104.14" y="101.6" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="J6" gate="G$1" pin="IN"/>
<wire x1="45.72" y1="101.6" x2="38.1" y2="101.6" width="0.1524" layer="91"/>
<label x="38.1" y="101.6" size="1.27" layer="95" rot="R180"/>
</segment>
</net>
<net name="SW1" class="0">
<segment>
<pinref part="U1" gate="G$1" pin="IO32"/>
<wire x1="111.76" y1="109.22" x2="104.14" y2="109.22" width="0.1524" layer="91"/>
<label x="104.14" y="109.22" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="J7" gate="G$1" pin="SW1"/>
<wire x1="45.72" y1="83.82" x2="38.1" y2="83.82" width="0.1524" layer="91"/>
<label x="38.1" y="83.82" size="1.27" layer="95" rot="R180"/>
</segment>
</net>
<net name="SW2" class="0">
<segment>
<pinref part="U1" gate="G$1" pin="IO33"/>
<wire x1="111.76" y1="106.68" x2="104.14" y2="106.68" width="0.1524" layer="91"/>
<label x="104.14" y="106.68" size="1.27" layer="95" rot="R180"/>
</segment>
<segment>
<pinref part="J7" gate="G$1" pin="SW2"/>
<wire x1="45.72" y1="81.28" x2="38.1" y2="81.28" width="0.1524" layer="91"/>
<label x="38.1" y="81.28" size="1.27" layer="95" rot="R180"/>
</segment>
</net>
<net name="SDA_3V3" class="0">
<segment>
<pinref part="U1" gate="G$1" pin="IO22"/>
<wire x1="142.24" y1="119.38" x2="149.86" y2="119.38" width="0.1524" layer="91"/>
<label x="149.86" y="119.38" size="1.27" layer="95" rot="R0"/>
</segment>
<segment>
<pinref part="U2" gate="G$1" pin="LV1"/>
<wire x1="152.4" y1="55.88" x2="144.78" y2="55.88" width="0.1524" layer="91"/>
<label x="144.78" y="55.88" size="1.27" layer="95" rot="R180"/>
</segment>
</net>
<net name="SCL_3V3" class="0">
<segment>
<pinref part="U1" gate="G$1" pin="IO23"/>
<wire x1="142.24" y1="121.92" x2="149.86" y2="121.92" width="0.1524" layer="91"/>
<label x="149.86" y="121.92" size="1.27" layer="95" rot="R0"/>
</segment>
<segment>
<pinref part="U2" gate="G$1" pin="LV2"/>
<wire x1="152.4" y1="53.34" x2="144.78" y2="53.34" width="0.1524" layer="91"/>
<label x="144.78" y="53.34" size="1.27" layer="95" rot="R180"/>
</segment>
</net>
<net name="SDA_5V" class="0">
<segment>
<pinref part="U2" gate="G$1" pin="HV1"/>
<wire x1="177.8" y1="55.88" x2="185.42" y2="55.88" width="0.1524" layer="91"/>
<label x="185.42" y="55.88" size="1.27" layer="95" rot="R0"/>
</segment>
<segment>
<pinref part="J4" gate="G$1" pin="SDA"/>
<wire x1="104.14" y1="48.26" x2="96.52" y2="48.26" width="0.1524" layer="91"/>
<label x="96.52" y="48.26" size="1.27" layer="95" rot="R180"/>
</segment>
</net>
<net name="SCL_5V" class="0">
<segment>
<pinref part="U2" gate="G$1" pin="HV2"/>
<wire x1="177.8" y1="53.34" x2="185.42" y2="53.34" width="0.1524" layer="91"/>
<label x="185.42" y="53.34" size="1.27" layer="95" rot="R0"/>
</segment>
<segment>
<pinref part="J4" gate="G$1" pin="SCL"/>
<wire x1="104.14" y1="45.72" x2="96.52" y2="45.72" width="0.1524" layer="91"/>
<label x="96.52" y="45.72" size="1.27" layer="95" rot="R180"/>
</segment>
</net>
</nets></sheet></sheets>
</schematic></drawing></eagle>
