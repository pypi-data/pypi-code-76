        Matrices = {}

        for n_pos in [6, 9, 15]:

            Matrices[n_pos] = {}

            A = np.zeros((n_pos * 3, 6), 'f')

            if n_pos == 6:
                positions = [[0., 0., 1.], [90., 0., 1.], [0., 90., 1.],
                             [180., 0., 1.], [270., 0., 1.], [0., -90., 1.]]

            if n_pos == 15:
                positions = [[315., 0., 1.], [225., 0., 1.], [180., 0., 1.], [135., 0., 1.], [45., 0., 1.],
                             [90., -45., 1.], [270., -45., 1.], [270.,
                                                                 0., 1.], [270., 45., 1.], [90., 45., 1.],
                             [180., 45., 1.], [180., -45., 1.], [0., -90., 1.], [0, -45., 1.], [0, 45., 1.]]
            if n_pos == 9:
                positions = [[315., 0., 1.], [225., 0., 1.], [180., 0., 1.],
                             [90., -45., 1.], [270., -45., 1.], [270., 0., 1.],
                             [180., 45., 1.], [180., -45., 1.], [0., -90., 1.]]

            tmpH = np.zeros((n_pos, 3), 'f')  # define tmpH
            for i in range(len(positions)):
                CART = pmag.dir2cart(positions[i])
                a = CART[0]
                b = CART[1]
                c = CART[2]
                A[3 * i][0] = a
                A[3 * i][3] = b
                A[3 * i][5] = c

                A[3 * i + 1][1] = b
                A[3 * i + 1][3] = a
                A[3 * i + 1][4] = c

                A[3 * i + 2][2] = c
                A[3 * i + 2][4] = b
                A[3 * i + 2][5] = a

                tmpH[i][0] = CART[0]
                tmpH[i][1] = CART[1]
                tmpH[i][2] = CART[2]

            B = np.dot(inv(np.dot(A.transpose(), A)), A.transpose())

            Matrices[n_pos]['A'] = A
            Matrices[n_pos]['B'] = B
            Matrices[n_pos]['tmpH'] = tmpH
