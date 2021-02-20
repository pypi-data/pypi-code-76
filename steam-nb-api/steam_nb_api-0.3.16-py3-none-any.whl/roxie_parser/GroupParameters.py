import numpy as np
from steam_nb_api.roxie_parser.BlockParameters import BlockParameters


class GroupParameters:
    '''
        Class of group parameters
    '''

    def __init__(self, noGroup, symm, typexy, blocks):
        self.noGroup = noGroup
        self.symm = symm
        self.typexy = typexy
        self.blocks = blocks

    def toString(self):
        return "{}, {}, {}, {}".format(self.noGroup, self.symm, self.typexy, self.blocks)

    def applyMultipoleSymmetry(self, blockParametersList: list, N: int, verbose: bool = False) -> list:
        '''
            **Apply N-order multipole symmetry to a list of BlockParameters objects**

            Function returns the input list of BlockParameters objects with new BlockParameters objects appended

            :param blockParametersList: list of BlockParameters containing information about the block to which applying the symmetry
            :type blockParametersList: list
            :param N: symmetry order (N=1: Dipole; N=2: Quadrupole; N=3: Sextupole;...)
            :type N: int
            :param verbose: flag that determines whether the output are printed
            :type verbose: bool

            :return: list
        '''

        symm = self.symm
        typexy = self.typexy
        blocks = self.blocks

        # This index will increase with each added block
        nb = len(blockParametersList)

        # Blocks to add to the attribute group.blocks
        blockToAddToGroup = []

        # Apply multipole geometry
        if typexy == 0:
            print('typexy = {}: No symmetry action.'.format(typexy))

        elif typexy == 1:
            print('typexy = {}: All.'.format(typexy))

            for b, additionalBlock in enumerate(blocks):
                idxBlock = additionalBlock - 1
                if verbose:
                    print('additionalBlock = {}'.format(additionalBlock))
                    print('pole={} of {}'.format(1, 2 * N))

                block = blockParametersList[idxBlock]
                # Add return block to the original block
                nb += 1
                blockParametersList.append(block.makeReturnBlock(N, n=nb))

                # Add return-line block index to group parameter list
                blockToAddToGroup = blockToAddToGroup + [nb]

                # This variable will switch between +1 and -1 for each pole
                signCurrent = +1

                # Add symmetric blocks
                for p in range(1, 2 * N - 1 + 1):
                    if verbose:
                        print('pole={} of {}'.format(p + 1, 2 * N))

                    # Update current sign for this pole
                    signCurrent = signCurrent - 2 * np.sign(signCurrent)

                    # Add go-line block
                    nb += 1
                    tempBlock = BlockParameters(noBlock=nb,
                                                typeBlock=blockParametersList[idxBlock].typeBlock,
                                                nco=blockParametersList[idxBlock].nco,
                                                radius=blockParametersList[idxBlock].radius,
                                                phi=blockParametersList[idxBlock].phi,
                                                alpha=blockParametersList[idxBlock].alpha,
                                                current=blockParametersList[idxBlock].current * signCurrent,
                                                # NOTE THE CHANGE
                                                condname=blockParametersList[idxBlock].condname,
                                                n1=blockParametersList[idxBlock].n1,
                                                n2=blockParametersList[idxBlock].n2,
                                                imag=blockParametersList[idxBlock].imag,
                                                turn=blockParametersList[idxBlock].turn + 360 / (2 * N) * p,
                                                # NOTE THE CHANGE
                                                )
                    blockParametersList.append(tempBlock)

                    # Add return-line block index to group parameter list
                    blockToAddToGroup = blockToAddToGroup + [nb]

                    # Add return-line block to block parameter list
                    nb += 1
                    blockParametersList.append(tempBlock.makeReturnBlock(N, n=nb))

                    # Add return-line block index to group parameter list
                    blockToAddToGroup = blockToAddToGroup + [nb]

        elif typexy == 2:
            print('typexy = {}: One coil.'.format(typexy))

            for b, additionalBlock in enumerate(blocks):
                idxBlock = additionalBlock - 1
                if verbose:
                    print('additionalBlock = {}'.format(additionalBlock))

                block = blockParametersList[idxBlock]
                nb += 1
                blockParametersList.append(block.makeReturnBlock(N, n=nb))

                # Add return-line block index to group parameter list
                blockToAddToGroup = blockToAddToGroup + [nb]

        elif typexy == 3:
            print('typexy = {}: Connection side: NOT SUPPORTED.'.format(typexy))

        else:
            print('typexy = {}: NOT SUPPORTED.'.format(typexy))

        self.blocks = self.blocks + blockToAddToGroup

        return blockParametersList