from moviepy.editor import *
from moviepy.audio.fx.volumex import volumex




class EditVideo:
    def __init__(self, filename):
        self.video = VideoFileClip(filename)

    def editVideo(self, cuts, titleText, folderName, isBoosted=False, threads=12):
        # print(filename)
        start_time = '00:00:00.00'
        clips = []

        for cut in cuts:
            print(cut)
            clip = self.video.subclip(start_time, cut[0])
            clips.append(clip)
            start_time = cut[1]

        if cuts[len(cuts) - 1][1] != 'end':
            clips.append(self.video.subclip(cuts[len(cuts) - 1][1]))

        txt_clip = (TextClip(titleText, fontsize=70, color='white')
                    .set_position('center')
                    .set_duration(5))

        final = concatenate_videoclips(clips)

        if isBoosted == 1:
            final = volumex(final, 2.0)

        final = CompositeVideoClip([final, txt_clip])

        final.write_videofile(folderName + '/' + titleText + '.mp4', fps=24, threads=threads)

        self.video.close()

    def getDuration(self):
        return self.video.duration

# def main():
    # cuts = [('00:01:18.00', '00:01:38.00'), ('00:02:46.00', '00:02:56.00'), ('00:14:25.00', '00:14:36.00'),
    #         ('00:15:17.00', '00:15:38.00'), ('00:21:10.00', '00:21:28.00'), ('00:25:16.00', 'end')]
    # editVideo('video1.mp4', cuts,  'lecture 01',12)

