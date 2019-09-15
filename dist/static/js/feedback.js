/*!
 * ======================================================
 * FeedBack Template For MUI (http://dev.dcloud.net.cn/mui)
 * =======================================================
 * @version:1.0.0
 * @author:cuihongbao@dcloud.io
 */
(function() {
    var index = 1;
    var size = null;
    var imageIndexIdNum = 0;
    var starIndex = 0;
    var feedback = {
        question: document.getElementById('question'),
        contact: document.getElementById('contact'),
        imageList: document.getElementById('image-list'),
        submitBtn: document.getElementById('submit')
    };
    var url = 'https://service.dcloud.net.cn/feedback';
    feedback.files = [];
    feedback.uploader = null;
    feedback.deviceInfo = null;
    mui.plusReady(function() {
        //璁惧淇℃伅锛屾棤闇€淇敼
        feedback.deviceInfo = {
            appid: plus.runtime.appid,
            imei: plus.device.imei, //璁惧鏍囪瘑
            images: feedback.files, //鍥剧墖鏂囦欢
            p: mui.os.android ? 'a' : 'i', //骞冲彴绫诲瀷锛宨琛ㄧずiOS骞冲彴锛宎琛ㄧずAndroid骞冲彴銆�
            md: plus.device.model, //璁惧鍨嬪彿
            app_version: plus.runtime.version,
            plus_version: plus.runtime.innerVersion, //鍩哄骇鐗堟湰鍙�
            os:  mui.os.version,
            net: ''+plus.networkinfo.getCurrentType()
        }
    });
    /**
     *鎻愪氦鎴愬姛涔嬪悗锛屾仮澶嶈〃鍗曢」
     */
    feedback.clearForm = function() {
        feedback.question.value = '';
        feedback.contact.value = '';
        feedback.imageList.innerHTML = '';
        feedback.newPlaceholder();
        feedback.files = [];
        index = 0;
        size = 0;
        imageIndexIdNum = 0;
        starIndex = 0;
        //娓呴櫎鎵€鏈夋槦鏍�
        mui('.icons i').each(function (index,element) {
            if (element.classList.contains('mui-icon-star-filled')) {
                element.classList.add('mui-icon-star')
                element.classList.remove('mui-icon-star-filled')
            }
        })
    };
    feedback.getFileInputArray = function() {
        return [].slice.call(feedback.imageList.querySelectorAll('.file'));
    };
    feedback.addFile = function(path) {
        feedback.files.push({name:"images"+index,path:path,id:"img-"+index});
        index++;
    };
    /**
     * 鍒濆鍖栧浘鐗囧煙鍗犱綅
     */
    feedback.newPlaceholder = function() {
        var fileInputArray = feedback.getFileInputArray();
        if (fileInputArray &&
            fileInputArray.length > 0 &&
            fileInputArray[fileInputArray.length - 1].parentNode.classList.contains('space')) {
            return;
        };
        imageIndexIdNum++;
        var placeholder = document.createElement('div');
        placeholder.setAttribute('class', 'image-item space');
        var up = document.createElement("div");
        up.setAttribute('class','image-up')
        //鍒犻櫎鍥剧墖
        var closeButton = document.createElement('div');
        closeButton.setAttribute('class', 'image-close');
        closeButton.innerHTML = 'X';
        closeButton.id = "img-"+index;
        //灏廥鐨勭偣鍑讳簨浠�
        closeButton.addEventListener('tap', function(event) {
            setTimeout(function() {
                for(var temp=0;temp<feedback.files.length;temp++){
                    if(feedback.files[temp].id==closeButton.id){
                        feedback.files.splice(temp,1);
                    }
                }
                feedback.imageList.removeChild(placeholder);
            }, 0);
            return false;
        }, false);

        //
        var fileInput = document.createElement('div');
        fileInput.setAttribute('class', 'file');
        fileInput.setAttribute('id', 'image-' + imageIndexIdNum);
        fileInput.addEventListener('tap', function(event) {
            var self = this;
            var index = (this.id).substr(-1);

            plus.gallery.pick(function(e) {
//				console.log("event:"+e);
                var name = e.substr(e.lastIndexOf('/') + 1);
                console.log("name:"+name);

                plus.zip.compressImage({
                    src: e,
                    dst: '_doc/' + name,
                    overwrite: true,
                    quality: 50
                }, function(zip) {
                    size += zip.size
                    console.log("filesize:"+zip.size+",totalsize:"+size);
                    if (size > (10*1024*1024)) {
                        return mui.toast('鏂囦欢瓒呭ぇ,璇烽噸鏂伴€夋嫨~');
                    }
                    if (!self.parentNode.classList.contains('space')) { //宸叉湁鍥剧墖
                        feedback.files.splice(index-1,1,{name:"images"+index,path:e});
                    } else { //鍔犲彿
                        placeholder.classList.remove('space');
                        feedback.addFile(zip.target);
                        feedback.newPlaceholder();
                    }
                    up.classList.remove('image-up');
                    placeholder.style.backgroundImage = 'url(' + zip.target + ')';
                }, function(zipe) {
                    mui.toast('鍘嬬缉澶辫触锛�')
                });



            }, function(e) {
                mui.toast(e.message);
            },{});
        }, false);
        placeholder.appendChild(closeButton);
        placeholder.appendChild(up);
        placeholder.appendChild(fileInput);
        feedback.imageList.appendChild(placeholder);
    };
    feedback.newPlaceholder();
    feedback.submitBtn.addEventListener('tap', function(event) {
        if (feedback.question.value == '' ||
            (feedback.contact.value != '' &&
                feedback.contact.value.search(/^(\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+)|([1-9]\d{4,9})$/) != 0)) {
            return mui.toast('淇℃伅濉啓涓嶇鍚堣鑼�');
        }
        if (feedback.question.value.length > 200 || feedback.contact.value.length > 200) {
            return mui.toast('淇℃伅瓒呴暱,璇烽噸鏂板～鍐檦')
        }
        //鍒ゆ柇缃戠粶杩炴帴
        if(plus.networkinfo.getCurrentType()==plus.networkinfo.CONNECTION_NONE){
            return mui.toast("杩炴帴缃戠粶澶辫触锛岃绋嶅悗鍐嶈瘯");
        }
        feedback.send(mui.extend({}, feedback.deviceInfo, {
            content: feedback.question.value,
            contact: feedback.contact.value,
            images: feedback.files,
            score:''+starIndex
        }))
    }, false)
    feedback.send = function(content) {
        feedback.uploader = plus.uploader.createUpload(url, {
            method: 'POST'
        }, function(upload, status) {
//			plus.nativeUI.closeWaiting()
            console.log("upload cb:"+upload.responseText);
            if(status==200){
                var data = JSON.parse(upload.responseText);
                //涓婁紶鎴愬姛锛岄噸缃〃鍗�
                if (data.ret === 0 && data.desc === 'Success') {
//					mui.toast('鍙嶉鎴愬姛~')
                    console.log("upload success");
//					feedback.clearForm();
                }
            }else{
                console.log("upload fail");
            }

        });
        //娣诲姞涓婁紶鏁版嵁
        mui.each(content, function(index, element) {
            if (index !== 'images') {
                console.log("addData:"+index+","+element);
//				console.log(index);
                feedback.uploader.addData(index, element)
            }
        });
        //娣诲姞涓婁紶鏂囦欢
        mui.each(feedback.files, function(index, element) {
            var f = feedback.files[index];
            console.log("addFile:"+JSON.stringify(f));
            feedback.uploader.addFile(f.path, {
                key: f.name
            });
        });
        //寮€濮嬩笂浼犱换鍔�
        feedback.uploader.start();
        mui.alert("鎰熻阿鍙嶉锛岀偣鍑荤‘瀹氬叧闂�","闂鍙嶉","纭畾",function () {
            feedback.clearForm();
            mui.back();
        });
//		plus.nativeUI.showWaiting();
    };

    //搴旂敤璇勫垎
    mui('.icons').on('tap','i',function(){
        var index = parseInt(this.getAttribute("data-index"));
        var parent = this.parentNode;
        var children = parent.children;
        if(this.classList.contains("mui-icon-star")){
            for(var i=0;i<index;i++){
                children[i].classList.remove('mui-icon-star');
                children[i].classList.add('mui-icon-star-filled');
            }
        }else{
            for (var i = index; i < 5; i++) {
                children[i].classList.add('mui-icon-star')
                children[i].classList.remove('mui-icon-star-filled')
            }
        }
        starIndex = index;
    });
    //閫夋嫨蹇嵎杈撳叆
    mui('.mui-popover').on('tap','li',function(e){
        document.getElementById("question").value = document.getElementById("question").value + this.children[0].innerHTML;
        mui('.mui-popover').popover('toggle')
    })
})();