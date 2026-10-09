<itemlayout width="640" height="{{ vscale(380) }}">
    <control type="group">
        <posx>55</posx>
        <posy>{{ vscale(61) }}</posy>
        <control type="image">
            <posx>0</posx>
            <posy>{{ vscale(0) }}</posy>
            <width>610</width>
            <height>{{ vscale(300) }}</height>
            <texture border="12">script.plex/white-square-rounded.png</texture>
            <colordiffuse>80181D24</colordiffuse>
        </control>
        <control type="group">
            <visible>!String.IsEmpty(ListItem.Property(community))</visible>
            <control type="image">
                <posx>20</posx>
                <posy>{{ vscale(18) }}</posy>
                <width>70</width>
                <height>{{ vscale(70) }}</height>
                <texture diffuse="script.plex/masks/role.png">script.plex/thumb_fallbacks/role.png</texture>
                <colordiffuse>FFFFFFFF</colordiffuse>
            </control>
            <control type="image">
                <posx>20</posx>
                <posy>{{ vscale(18) }}</posy>
                <width>70</width>
                <height>{{ vscale(70) }}</height>
                <texture background="true" diffuse="script.plex/masks/role.png">$INFO[ListItem.Thumb]</texture>
                <colordiffuse>FFFFFFFF</colordiffuse>
            </control>
            <control type="label">
                <posx>108</posx>
                <posy>{{ vscale(20) }}</posy>
                <width>470</width>
                <height>{{ vscale(34) }}</height>
                <font>font10</font>
                <textcolor>DDFFFFFF</textcolor>
                <align>left</align>
                <label>$INFO[ListItem.Label]</label>
            </control>
            <control type="label">
                <posx>108</posx>
                <posy>{{ vscale(54) }}</posy>
                <width>470</width>
                <height>{{ vscale(30) }}</height>
                <font>font10</font>
                <textcolor>99FFFFFF</textcolor>
                <align>left</align>
                <label>$INFO[ListItem.Label2]</label>
            </control>
            <control type="image">
                <posx>195</posx>
                <posy>{{ vscale(126) }}</posy>
                <width>220</width>
                <height>{{ vscale(38) }}</height>
                <aspectratio>keep</aspectratio>
                <texture>$INFO[ListItem.Property(star.texture)]</texture>
            </control>
            <control type="textbox">
                <posx>25</posx>
                <posy>{{ vscale(176) }}</posy>
                <width>560</width>
                <height>{{ vscale(64) }}</height>
                <font>font10</font>
                <textcolor>DDFFFFFF</textcolor>
                <label>$INFO[ListItem.Property(text)]</label>
            </control>
            <control type="label">
                <posx>315</posx>
                <posy>{{ vscale(257) }}</posy>
                <width>280</width>
                <height>{{ vscale(32) }}</height>
                <font>font10</font>
                <textcolor>99FFFFFF</textcolor>
                <align>left</align>
                <label>$INFO[ListItem.Property(discussion)]</label>
            </control>
            <control type="image">
                <posx>25</posx>
                <posy>{{ vscale(257) }}</posy>
                <width>28</width>
                <height>{{ vscale(28) }}</height>
                <aspectratio>keep</aspectratio>
                <texture>$INFO[ListItem.Property(reaction.icon.0)]</texture>
            </control>
            <control type="image">
                <posx>52</posx>
                <posy>{{ vscale(257) }}</posy>
                <width>28</width>
                <height>{{ vscale(28) }}</height>
                <aspectratio>keep</aspectratio>
                <texture>$INFO[ListItem.Property(reaction.icon.1)]</texture>
            </control>
            <control type="image">
                <posx>79</posx>
                <posy>{{ vscale(257) }}</posy>
                <width>28</width>
                <height>{{ vscale(28) }}</height>
                <aspectratio>keep</aspectratio>
                <texture>$INFO[ListItem.Property(reaction.icon.2)]</texture>
            </control>
            <control type="label">
                <posx>118</posx>
                <posy>{{ vscale(257) }}</posy>
                <width>150</width>
                <height>{{ vscale(32) }}</height>
                <font>font10</font>
                <textcolor>DDFFFFFF</textcolor>
                <label>$INFO[ListItem.Property(reaction.count)]</label>
            </control>
            <control type="image">
                <posx>555</posx>
                <posy>{{ vscale(20) }}</posy>
                <width>32</width>
                <height>{{ vscale(32) }}</height>
                <aspectratio>keep</aspectratio>
                <texture>$INFO[ListItem.Property(reaction.mine)]</texture>
            </control>
        </control>
        <control type="group">
            <visible>String.IsEmpty(ListItem.Property(community))</visible>
            <control type="image">
                <posx>20</posx>
                <posy>{{ vscale(18) }}</posy>
                <width>70</width>
                <height>{{ vscale(70) }}</height>
                <texture>script.plex/reviews/$INFO[ListItem.Thumb].png</texture>
                <colordiffuse>FFFFFFFF</colordiffuse>
            </control>
            <control type="label">
                <posx>108</posx>
                <posy>{{ vscale(20) }}</posy>
                <width>470</width>
                <height>{{ vscale(34) }}</height>
                <font>font10</font>
                <textcolor>DDFFFFFF</textcolor>
                <align>left</align>
                <label>$INFO[ListItem.Label]</label>
            </control>
            <control type="label">
                <posx>108</posx>
                <posy>{{ vscale(54) }}</posy>
                <width>470</width>
                <height>{{ vscale(30) }}</height>
                <font>font10</font>
                <textcolor>99FFFFFF</textcolor>
                <align>left</align>
                <label>$INFO[ListItem.Label2]</label>
            </control>
            <control type="textbox">
                <posx>25</posx>
                <posy>{{ vscale(116) }}</posy>
                <width>560</width>
                <height>{{ vscale(162) }}</height>
                <font>font10</font>
                <textcolor>DDFFFFFF</textcolor>
                <label>$INFO[ListItem.Property(text)]</label>
            </control>
        </control>
    </control>
</itemlayout>
<focusedlayout width="640" height="{{ vscale(380) }}">
    <control type="group">
        <posx>55</posx>
        <posy>{{ vscale(61) }}</posy>
        <control type="image">
            <posx>0</posx>
            <posy>{{ vscale(0) }}</posy>
            <width>610</width>
            <height>{{ vscale(300) }}</height>
            <texture border="12">script.plex/white-square-rounded.png</texture>
            <colordiffuse>A0181D24</colordiffuse>
        </control>
        <control type="group">
            <visible>!String.IsEmpty(ListItem.Property(community))</visible>
            <control type="image">
                <posx>20</posx>
                <posy>{{ vscale(18) }}</posy>
                <width>70</width>
                <height>{{ vscale(70) }}</height>
                <texture diffuse="script.plex/masks/role.png">script.plex/thumb_fallbacks/role.png</texture>
                <colordiffuse>FFFFFFFF</colordiffuse>
            </control>
            <control type="image">
                <posx>20</posx>
                <posy>{{ vscale(18) }}</posy>
                <width>70</width>
                <height>{{ vscale(70) }}</height>
                <texture background="true" diffuse="script.plex/masks/role.png">$INFO[ListItem.Thumb]</texture>
                <colordiffuse>FFFFFFFF</colordiffuse>
            </control>
            <control type="label">
                <posx>108</posx>
                <posy>{{ vscale(20) }}</posy>
                <width>470</width>
                <height>{{ vscale(34) }}</height>
                <font>font10</font>
                <textcolor>DDFFFFFF</textcolor>
                <align>left</align>
                <label>$INFO[ListItem.Label]</label>
            </control>
            <control type="label">
                <posx>108</posx>
                <posy>{{ vscale(54) }}</posy>
                <width>470</width>
                <height>{{ vscale(30) }}</height>
                <font>font10</font>
                <textcolor>99FFFFFF</textcolor>
                <align>left</align>
                <label>$INFO[ListItem.Label2]</label>
            </control>
            <control type="image">
                <posx>195</posx>
                <posy>{{ vscale(126) }}</posy>
                <width>220</width>
                <height>{{ vscale(38) }}</height>
                <aspectratio>keep</aspectratio>
                <texture>$INFO[ListItem.Property(star.texture)]</texture>
            </control>
            <control type="textbox">
                <posx>25</posx>
                <posy>{{ vscale(176) }}</posy>
                <width>560</width>
                <height>{{ vscale(64) }}</height>
                <font>font10</font>
                <textcolor>DDFFFFFF</textcolor>
                <label>$INFO[ListItem.Property(text)]</label>
            </control>
            <control type="label">
                <posx>315</posx>
                <posy>{{ vscale(257) }}</posy>
                <width>280</width>
                <height>{{ vscale(32) }}</height>
                <font>font10</font>
                <textcolor>99FFFFFF</textcolor>
                <align>left</align>
                <label>$INFO[ListItem.Property(discussion)]</label>
            </control>
            <control type="image">
                <posx>25</posx>
                <posy>{{ vscale(257) }}</posy>
                <width>28</width>
                <height>{{ vscale(28) }}</height>
                <aspectratio>keep</aspectratio>
                <texture>$INFO[ListItem.Property(reaction.icon.0)]</texture>
            </control>
            <control type="image">
                <posx>52</posx>
                <posy>{{ vscale(257) }}</posy>
                <width>28</width>
                <height>{{ vscale(28) }}</height>
                <aspectratio>keep</aspectratio>
                <texture>$INFO[ListItem.Property(reaction.icon.1)]</texture>
            </control>
            <control type="image">
                <posx>79</posx>
                <posy>{{ vscale(257) }}</posy>
                <width>28</width>
                <height>{{ vscale(28) }}</height>
                <aspectratio>keep</aspectratio>
                <texture>$INFO[ListItem.Property(reaction.icon.2)]</texture>
            </control>
            <control type="label">
                <posx>118</posx>
                <posy>{{ vscale(257) }}</posy>
                <width>150</width>
                <height>{{ vscale(32) }}</height>
                <font>font10</font>
                <textcolor>DDFFFFFF</textcolor>
                <label>$INFO[ListItem.Property(reaction.count)]</label>
            </control>
            <control type="image">
                <posx>555</posx>
                <posy>{{ vscale(20) }}</posy>
                <width>32</width>
                <height>{{ vscale(32) }}</height>
                <aspectratio>keep</aspectratio>
                <texture>$INFO[ListItem.Property(reaction.mine)]</texture>
            </control>
        </control>
        <control type="group">
            <visible>String.IsEmpty(ListItem.Property(community))</visible>
            <control type="image">
                <posx>20</posx>
                <posy>{{ vscale(18) }}</posy>
                <width>70</width>
                <height>{{ vscale(70) }}</height>
                <texture>script.plex/reviews/$INFO[ListItem.Thumb].png</texture>
                <colordiffuse>FFFFFFFF</colordiffuse>
            </control>
            <control type="label">
                <posx>108</posx>
                <posy>{{ vscale(20) }}</posy>
                <width>470</width>
                <height>{{ vscale(34) }}</height>
                <font>font10</font>
                <textcolor>DDFFFFFF</textcolor>
                <align>left</align>
                <label>$INFO[ListItem.Label]</label>
            </control>
            <control type="label">
                <posx>108</posx>
                <posy>{{ vscale(54) }}</posy>
                <width>470</width>
                <height>{{ vscale(30) }}</height>
                <font>font10</font>
                <textcolor>99FFFFFF</textcolor>
                <align>left</align>
                <label>$INFO[ListItem.Label2]</label>
            </control>
            <control type="textbox">
                <posx>25</posx>
                <posy>{{ vscale(116) }}</posy>
                <width>560</width>
                <height>{{ vscale(162) }}</height>
                <font>font10</font>
                <textcolor>DDFFFFFF</textcolor>
                <label>$INFO[ListItem.Property(text)]</label>
            </control>
        </control>
        <control type="image">
            <visible>Control.HasFocus(401)</visible>
            <posx>-3</posx>
            <posy>{{ vscale(-3) }}</posy>
            <width>616</width>
            <height>{{ vscale(306) }}</height>
            <texture border="12">script.plex/white-outline-rounded.png</texture>
            <colordiffuse>FFFFFFFF</colordiffuse>
        </control>
    </control>
</focusedlayout>
