        # pivot korbowodu2 (stały punkt)
        Px, Py = self.korbowod2.x, self.korbowod2.y  

        # punkt, do którego chcemy podążać (zaczepienie korbowodu3 / kolo)
        Bx, By = self.kolo.punkt_zaczepienia()  

        # długość ramienia korbowodu2
        Lx = self.korbowod2.koniec[0] - Px
        Ly = self.korbowod2.koniec[1] - Py
        L = math.hypot(Lx, Ly)

        # wektor od pivot do celu
        dx = Bx - Px
        dy = By - Py
        d = math.hypot(dx, dy)

        # jeśli cel poza zasięgiem ramienia, ograniczamy
        if d > L:
            dx *= L/d
            dy *= L/d
            d = L

        # kąt ramienia względem osi X
        alpha = math.atan2(dy, dx)

        # ustaw kąt sztywnego korbowodu
        self.korbowod2.ustaw_kat(math.degrees(alpha))

        # przelicz faktyczne współrzędne końca
        x_end = Px + L * math.cos(alpha)
        y_end = Py + L * math.sin(alpha)
        self.korbowod2.koniec = (x_end, y_end)