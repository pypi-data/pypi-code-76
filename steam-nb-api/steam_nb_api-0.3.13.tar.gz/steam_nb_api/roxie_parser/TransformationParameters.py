class TransformationParameters:
    '''
        Class of transformation parameters
    '''

    def __init__(self, noTransformation, x, y, alph, bet, string, act, bcs):
        self.noTransformation = noTransformation
        self.x = x
        self.y = y
        self.alph = alph
        self.bet = bet
        self.string = string
        self.act = act
        self.bcs = bcs

    def toString(self):
        return "{}, {}, {}, {}, {}, {}, {}, {}".format(self.noTransformation, self.x, self.y, self.alph, self.bet,
                                                       self.string, self.act, self.bcs)

    def applyTranformationShift2(self, blockParametersList, groupParametersList, verbose: bool = False):
        '''
            **Apply shift2 transformation (shift in x and y direction) to a list of BlockParameters objects**

            Function returns the input list of BlockParameters objects with the attributes shift2 set to new values

            :param blockParametersList: list of BlockParameters containing information about the block to which applying the transformation
            :type blockParametersList: list
            :param groupParametersList: list of GroupParameters containing information about the group to which applying the transformation
            :type groupParametersList: list

            :return: list
        '''

        x = self.x
        y = self.y
        alph = self.alph
        bet = self.bet
        string = self.string
        act = self.act
        bcs = self.bcs

        # Apply shift2 transformation
        if act == 0:
            if verbose: print('Act on All blocks.')
            for block in blockParametersList:
                block.setBlockShift2([x, y])

        if act == 1:
            if verbose: print('Act on All blocks of these groups: {}.'.format(bcs))
            for group in groupParametersList:
                if verbose: print('group={}'.format(group.noGroup))
                if group.noGroup in bcs:
                    for block in blockParametersList:
                        if verbose: print('block={}'.format(block.noBlock))
                        if block.noBlock in group.blocks:
                            block.setBlockShift2([x, y])

        if act == 2:
            if verbose: print('Act on Parent and offspring blocks of these groups {}: Not supported!'.format(bcs))

        if act == 3:
            if verbose: print('Act on Specified block only: Block {}'.format(bcs))
            for block in blockParametersList:
                if block.noBlock in bcs:
                    block.setBlockShift2([x, y])

        if act == 4:
            if verbose: print('Act on Conductors {}. Not supported!'.format(bcs))

        if act == 9:
            if verbose: print('Act on N/a: Not supported!')

        return blockParametersList

    def applyTranformationRoll2(self, blockParametersList, groupParametersList, verbose: bool = False):
        '''
            **Apply roll2 transformation (counterclockwise rotation) to a list of BlockParameters objects**

            Function returns the input list of BlockParameters objects with the attributes roll2 set to new values

            :param blockParametersList: list of BlockParameters containing information about the block to which applying the transformation
            :type blockParametersList: list
            :param groupParametersList: list of GroupParameters containing information about the group to which applying the transformation
            :type groupParametersList: list

            :return: list
        '''

        x = self.x
        y = self.y
        alph = self.alph
        bet = self.bet
        string = self.string
        act = self.act
        bcs = self.bcs

        # Apply roll2 transformation
        if act == 0:
            if verbose: print('Act on All blocks.')
            for block in blockParametersList:
                block.setBlockRoll2([x, y, alph])

        if act == 1:
            if verbose: print('Act on All blocks of these groups: {}.'.format(bcs))
            for group in groupParametersList:
                if group.noGroup in bcs:
                    for block in blockParametersList:
                        if block.noBlock in group.blocks:
                            block.setBlockRoll2([x, y, alph])

        if act == 2:
            if verbose: print('Act on Parent and offspring blocks of these groups {}: Not supported!'.format(bcs))

        if act == 3:
            if verbose: print('Act on Specified block only: Block {}'.format(bcs))
            for block in blockParametersList:
                if block.noBlock in bcs:
                    block.setBlockRoll2([x, y, alph])

        if act == 4:
            if verbose: print('Act on Conductors {}. Not supported!'.format(bcs))

        if act == 9:
            if verbose: print('Act on N/a: Not supported!')

        return blockParametersList