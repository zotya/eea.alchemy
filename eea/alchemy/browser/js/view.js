if (typeof String.prototype.endswith !== 'function') {
  String.prototype.endswith = function(suffix) {
      return this.indexOf(suffix, this.length - suffix.length) !== -1;
  };
}

if(window.EEA === undefined){
  var EEA = {
    who: 'eea.alchemy',
    version: '5.0'
  };
}

EEA.Highlighter = function(context, options){
 var self = this;
  self.context = context;

  self.settings = {
    highlightClass: 'eea-alchemy-tag'
  };

  if(options){
    jQuery.extend(self.settings, options);
  }

  self.initialize();
};

EEA.Highlighter.prototype = {
  initialize: function(){

  }
};

EEA.Alchemy = function(context, options){
  var self = this;
  self.context = context;

  self.settings = {
    api: 'alchemy.tags.json',
    highlightClass: 'eea-alchemy-tag'
  };

  if(options){
    jQuery.extend(self.settings, options);
  }

  try{
    self.initialize();
  }catch(err){
    if(window.console){
      console.log(err);
    }
  }
};

EEA.Alchemy.prototype = {
  initialize: function(){
    var self = this;
    jQuery.ajax({
      dataType: "json",
      url: self.settings.api,
      success: function(data){
        self.onSuccess(data);
      }
    });
  },

  onSuccess: function(options){
    var self = this;

    // Auto-tagging is not enabled
    if(!options.enabled){
      return;
    }

    // Nothing to search
    if(!options.search){
      return;
    }

    jQuery.extend(self.settings, options);
    return self.reload();
  },

  reload: function(){
    var self = this;
    var adapter = new EEA.Highlighter(self.context, self.settings);
    self.context.data('EEAHighlighter', adapter);
    //jQuery('.' + self.settings.highlightClass, self.context).each(function(){
      //return self.reloadItem(jQuery(this));
    //});
  }

  //reloadItem: function(item){
    //var self = this;

    //// Skip blacklisted items
    //var blacklist = self.settings.blacklist || [];
    //blacklist.push('a');
    //blacklist = blacklist.join(',');

    //if(item.parents(blacklist).length){
      //item.removeClass(self.settings.highlightClass);
      //return;
    //}

    //var url = self.settings.search[item.text()];
    //if(!url){
      //return;
    //}

    //var link = jQuery('<a>')
      //.attr('href', url + item.text())
      //.text(item.text());
    //item.html(link);
    //item.show('highlight', 2000);
  //}
};

jQuery.fn.EEAlchemy = function(options){
  return this.each(function(){
    var context = jQuery(this);
    var adapter = new EEA.Alchemy(context, options);
    context.data('EEAlchemy', adapter);
  });
};

// On document ready
jQuery(document).ready(function(){
  var enabled = jQuery('#eea-alchemy-enabled');
  if(!enabled.length){
    return;
  }

  var items = jQuery('#region-content,#content');
  if(!items.length){
    return;
  }

  base = jQuery('base').attr('href') || '';

  if(base && !base.endswith('/view')){
    base = base.replace(/\/view$/g, '/');
  }

  if(base && !base.endswith('/')){
    base += '/';
  }

  items.EEAlchemy({
    api: base + 'alchemy.tags.json'
  });

});
