#include <iostream>


struct Note {
    double start, end;
    unsigned char note, velocity;
};

std::ostream& operator<<(std::ostream& os, const Note& note) {
    os << "Note(start=" << note.start << ", end=" << note.end
        << ", note=" << +note.note << ", velocity=" << +note.velocity
        << ")";
    return os;
}


/**
 * Unserialize MIDI notes according to docs.
 */
struct Midi {
    const int note_size = 2*8 + 2*1;

    int count;
    char* data;

    Midi(char* data) {
        count = *(int*)(data);
        this->data = data + 4;
    }

    Note get(int i) {
        char* d = data + i*note_size;
        Note n;
        n.start = *(double*)(d);
        n.end = *(double*)(d+8);
        n.note = *(unsigned char*)(d+16);
        n.velocity = *(unsigned char*)(d+17);

        return n;
    }

    Note operator[](int i) {
        return get(i);
    }
};
