//
//  PianoRay
//  Video rendering pipeline with piano visualization.
//  Copyright  PianoRay Authors  2022
//
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with this program.  If not, see <https://www.gnu.org/licenses/>.
//

import org.junit.*;
import static org.junit.Assert.*;


public class JUTest {
    private Printer p1, p2, p3;

    @Before
    public void init() {
        p1 = new Printer(2);
        p2 = new Printer(20);
        p3 = new Printer(-20);
    }

    @Test
    public void testPrinter() {
        assertTrue(p1.getStr().equals("[2, 3, 4]"));
        assertTrue(p2.getStr().equals("[20, 21, 22]"));
        assertTrue(p3.getStr().equals("[-20, -19, -18]"));
        assertTrue(false);
    }

    public static void main(String args[]) {
        org.junit.runner.JUnitCore.main("JUTest");
    }
}
