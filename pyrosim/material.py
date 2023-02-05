from pyrosim.commonFunctions import Save_Whitespace

class MATERIAL: 

    def __init__(self, rgba: list[float]):
        color_str = str(rgba[0]) + ' ' + str(rgba[1]) + ' ' + str(rgba[2]) + ' ' + str(rgba[3])

        self.depth  = 3

        self.string1 = '<material name="' + color_str + '">'

        self.string2 = '    <color rgba="' + color_str + '"/>'

        self.string3 = '</material>'

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )
