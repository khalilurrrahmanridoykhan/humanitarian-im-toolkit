<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.34" styleCategories="Symbology">
  <renderer-v2 type="graduatedSymbol" attr="needs_score" graduatedMethod="GraduatedColor">
    <ranges>
      <range label="0 - 20 (low)" lower="0" upper="20" render="true" symbol="0"/>
      <range label="20 - 40" lower="20" upper="40" render="true" symbol="1"/>
      <range label="40 - 60 (moderate)" lower="40" upper="60" render="true" symbol="2"/>
      <range label="60 - 80" lower="60" upper="80" render="true" symbol="3"/>
      <range label="80 - 100 (severe)" lower="80" upper="100" render="true" symbol="4"/>
    </ranges>
    <symbols>
      <symbol type="fill" name="0"><layer class="SimpleFill"><Option><Option type="QString" name="color" value="255,255,204,255"/><Option type="QString" name="outline_color" value="0,0,0,255"/><Option type="QString" name="outline_width" value="0.26"/></Option></layer></symbol>
      <symbol type="fill" name="1"><layer class="SimpleFill"><Option><Option type="QString" name="color" value="254,217,142,255"/><Option type="QString" name="outline_color" value="0,0,0,255"/><Option type="QString" name="outline_width" value="0.26"/></Option></layer></symbol>
      <symbol type="fill" name="2"><layer class="SimpleFill"><Option><Option type="QString" name="color" value="254,153,41,255"/><Option type="QString" name="outline_color" value="0,0,0,255"/><Option type="QString" name="outline_width" value="0.26"/></Option></layer></symbol>
      <symbol type="fill" name="3"><layer class="SimpleFill"><Option><Option type="QString" name="color" value="217,95,14,255"/><Option type="QString" name="outline_color" value="0,0,0,255"/><Option type="QString" name="outline_width" value="0.26"/></Option></layer></symbol>
      <symbol type="fill" name="4"><layer class="SimpleFill"><Option><Option type="QString" name="color" value="153,52,4,255"/><Option type="QString" name="outline_color" value="0,0,0,255"/><Option type="QString" name="outline_width" value="0.26"/></Option></layer></symbol>
    </symbols>
  </renderer-v2>
</qgis>
